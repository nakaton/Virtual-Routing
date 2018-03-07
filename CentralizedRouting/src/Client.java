import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

public class Client {
    //route就是客户端从服务端获得的路由信息，保存到本地的数据
	private static boolean  t = false;
	private static Map<String,String> route = new HashMap<>();
    public static void main(String[] args) throws IOException {
    	//String message = new String("172.18.157.155,10;172.18.157.200,5");
        new Thread(new Runnable() {
        	public void run() {
                //向服务器发送数据的线程
        		sendMess();
        	}
        }).start();
        new Thread(new Runnable() {
        	public void run() {
                //从服务器接受数据的线程
        		recvMess();
        	}
        }).start();
    }
    private static void sendMess() {
    	try {
            Socket socket = new Socket("172.18.157.89", 1234);
            System.out.println("客户端启动成功");

            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
            PrintWriter write = new PrintWriter(socket.getOutputStream());
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            String readline;
            int read;
            String localHost = "" +  InetAddress.getLocalHost().getHostAddress();
            
            Gson gson = new Gson(); 
            
            //只有输入“end"的时候循环会停止，socket关闭
            //否则客户端会随时接受输入，发送给服务端
            while(true) {
            	Map<String, Object> temp = new HashMap<String, Object>();
            	
            	System.out.println("Destination ip: ");
            	readline = br.readLine();
            	if(readline.equals("end")) break;
            	
            	temp.put("to", readline);
            	
            	System.out.println("Cost to "+readline+" is: ");
            	readline =br.readLine();
            	temp.put("cost", readline);
            	
            	if(readline.equals("end")) break;
            	
            	temp.put("from", localHost);
            	write.println(gson.toJson(temp));
            	write.flush();
            	
            	System.out.println(gson.toJson(temp));
            }

            write.close();
            in.close();
            socket.close();
            //exit();
        } catch (Exception e) {
            System.out.println("can not listen to:" + e);
        }
    }
    private static void recvMess() {
    	try {
    		ServerSocket server = null;
    		server = new ServerSocket(1234);
    		System.out.println("客户端开始监听服务器返回的路由信息！");
    		
    		while(true) {
    			Socket socket2 = server.accept();
                //在此阻塞，当接收到服务端发来的信息时，就new一个线程处理发来的数据。
                //在死循环内一直监听
        		new Thread(new Runnable() {
        			public void run() {
        				try{
        					String readin;
            	            BufferedReader in2=new BufferedReader(new InputStreamReader(socket2.getInputStream()));
            	            	
            	            readin = in2.readLine();
        	                             
        	                java.lang.reflect.Type mapType = new TypeToken<Map<String, String>>(){}.getType();
        	            	Gson gson = new Gson();
        	            	Map<String, String> info = gson.fromJson(readin, mapType );
        	            	
        	            	route = info;

                            //输出从服务端得到的路由信息
        	            	System.out.println(readin);
            	            
            	            socket2.close();
            	            in2.close();
        				}catch(Exception e) {
        					System.out.println("Error:"+e);
        				}
        			}
        		}).start();
        		if(t)break;
    		}
    		server.close();
    	}catch(Exception e) {
    		System.out.println("Error:"+e);
    	}
    }
}