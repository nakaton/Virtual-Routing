
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

public class Server {
    /*nextNode:下一跳矩阵，nextNode[i][j]表示从节点i发送数据到节点j的最短路径的下一跳节点
    **cost:最小代价矩阵，cost[i][j]表示从节点i到节点j的最短路径的代价
    **toInt:将节点的ip对应到一个int值，这个int值会用在nextNode和cost矩阵中表示该节点
    **toString:和toInt是相反的，toString.get(i)-->获取节点i的ip地址
    **set:存储了所有在拓扑图中的节点
    **pos:所有在图谱图中的节点的个数
    */
    private boolean t = false;
    private static int[][] nextNode = new int[100][100], cost = new int[100][100];
    private Map<String,Integer> toInt = new HashMap<String,Integer>();
    private Map<Integer,String> toString = new HashMap<Integer,String>();
    public Set<String> set = new HashSet<String>();
    public int pos = 0;
    private static final int MAX = 10000, UNREACHABLE = -1;

    public static void main(String[] args) throws IOException{
        init();
        Server socketService = new Server();
        socketService.oneServer();
    }
    public void oneServer(){
        try{
            ServerSocket server=null;
            try{
                server=new ServerSocket(1234);
                System.out.println("服务器启动成功");
            }catch(Exception e) {
                    System.out.println("没有启动监听："+e);
            }
            while(true) {
                if(t)break;
                try{
                    Socket socket=server.accept();
                    /*在此阻塞，一旦有客户端发来信息，
                    **就new一个线程处理信息，
                    **本线程又通过死循环回到阻塞的地方，
                    **这样就可以同时处理很多个客户端的信息了
                    */
                    new Thread(new Runnable(){
                        public void run(){
                            try {
                                String readin;
                                BufferedReader in=new BufferedReader(new InputStreamReader(socket.getInputStream()));

                                while(true) {
                                    readin = in.readLine();                                    
                                    
                                    /*从socket的输入流获取客户端发送来的信息，
                                    **将json格式的数据转换成map
                                    */
                                    java.lang.reflect.Type mapType = new TypeToken<Map<String, Object>>(){}.getType();
                                    Gson gson = new Gson();
                                    Map<String, Object> info = gson.fromJson(readin, mapType );
                                    String from = (String)info.get("from");
                                    String to = (String)info.get("to");
                                    int co = Integer.parseInt((String)info.get("cost"));
                                    
                                    
                                    //set记录了所有在拓扑图中的客户端ip
                                    //pos记录了这些客户端的个数，
                                    //客户端第一次添加进拓扑图时的pos也相当于这些客户端的唯一id
                                    if(!set.contains(from)) {
                                        set.add(from);
                                        toInt.put(from,pos);
                                        toString.put(pos, from);
                                        pos += 1;
                                    }
                                    if(!set.contains(to)) {
                                        set.add(to);
                                        toInt.put(to,pos);
                                        toString.put(pos, to);
                                        pos += 1;
                                    }
                                    
                                    //将直接更新的数据更新到本地的数据中
                                    cost[toInt.get(from)][toInt.get(to)] = co;
                                    cost[toInt.get(to)][toInt.get(from)] = co;
                                    nextNode[toInt.get(from)][toInt.get(to)] = toInt.get(to);
                                    nextNode[toInt.get(to)][toInt.get(from)] = toInt.get(from);
                                    System.out.println(from+"===== "+to+" "+co+" "+pos);

                                    //Floyd算法计算最短路径
                                    floyd();
                                    

                                    //用多线程+socket通知所有在拓扑图中节点，向它们发送最新的路由信息
                                    for(int i = 0; i < pos; i++) {
                                        final int temp = i;
                                        new Thread(new Runnable(){
                                            public void run() {
                                                Map<String,String> re = new HashMap<>();
                                                String des = toString.get(temp);
                                                for(int j = 0; j < pos; j++) {
                                                    re.put(toString.get(j), toString.get(nextNode[temp][j]));
                                                }
                                                Gson gson = new Gson(); 
                                                String json = gson.toJson(re);
                                                
                                                try {
                                                    Socket socket = new Socket(des, 1234);
                                                    PrintWriter write = new PrintWriter(socket.getOutputStream());
                                                    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                                                    write.println(gson.toJson(temp));
                                                    write.flush();
                                                    
                                                    write.close();
                                                    in.close();
                                                    socket.close();
                                                }catch(Exception e) {
                                                    System.out.println("Error."+e);
                                                }

                                                System.out.print(des+"-->");
                                                System.out.println(json);
                                            }
                                        }).start();
                                    }

                                    //print函数输出此时的下一跳矩阵和最短路径矩阵，可以在服务端上查看此时的状态
                                    print();
                                    if(t)break;
                                }

                                in.close();
                                socket.close(); 
                            }catch(Exception e) {
                                System.out.println("Error."+e);
                            }
                        }
                    }).start();
                }catch(Exception e) {
                    System.out.println("Error."+e);
                }
            }
            server.close(); 
        }catch(Exception e) {
            System.out.println("Error."+e);
        }
    }
    private static void init() {
        for(int i = 0; i < 100; i++) {
            for(int j = 0; j < 100; j++) {
                if(i==j)
                    cost[i][j] = 0;
                else {
                    cost[i][j] = MAX;
                }
                nextNode[i][j] = UNREACHABLE;
            }
        }
    }
    private void floyd() {
        for(int k = 0; k < pos; k++){  
            for(int i = 0; i < pos; i++){  
                for(int j = 0; j < pos; j++){  
                    if(cost[i][k] < MAX && cost[k][j] < MAX && cost[i][j] > cost[i][k] + cost[k][j]){
                        cost[i][j] = cost[i][k] + cost[k][j];
                        nextNode[i][j] = k;  
                    }                    
                }  
            }  
        }  
    }
    private void print() {
        for(int i = 0; i < pos; i++){
            for(int j = 0; j <pos; j++){
                System.out.print(nextNode[i][j]+" ");
            }
            System.out.println("");
        }
        System.out.println("");
        for(int i = 0; i < pos; i++){
            for(int j = 0; j <pos; j++){
                System.out.print(cost[i][j]+" ");
            }
            System.out.println("");
        }
    }
}