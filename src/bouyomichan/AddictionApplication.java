package bouyomichan;

import py4j.GatewayServer;

/**
 * Created by b1016126 on 2017/05/23.
 */
public class AddictionApplication {
    public int addiction(int first, int second) {
        return first + second;
    }

    public static void main(String[] args) {
        BouyomiChan4J app = new BouyomiChan4J();
        // app を gateway.entry_point に設定
        GatewayServer server = new GatewayServer(app);
        server.start();
        System.out.println("Gateway Server Started");
    }

}
