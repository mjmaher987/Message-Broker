package sad.project;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.function.Function;

public class Consumer {
    private final static String PULL_URL = "http://localhost:8000/pull";

    public Message pull() {
        Message message = null;
        try {
            URL url = new URL(PULL_URL);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            int responseCode = connection.getResponseCode();
            System.out.println("Response Code: " + responseCode);

            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String inputLine;
            while ((inputLine = reader.readLine()) != null) {
                response.append(inputLine);
            }
            reader.close();

            Gson gson = new GsonBuilder().create();
            message = gson.fromJson(response.toString(), Message.class);

            System.out.println(message.toString());
            connection.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return message;
    }

    public void subscribe(Function<Message, Void> function, long intervalMillis) {
        Thread subscriberThread = getSubscriberThread(function, intervalMillis);
        subscriberThread.start();
    }


    private Thread getSubscriberThread(final Function<Message, Void> function, final long intervalMillis) {
        Thread subscriberThread = new Thread(() -> {
            while (true) {
                try {
                    Message message = pull();
                    function.apply(message);

                    Thread.sleep(intervalMillis);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        return subscriberThread;
    }
}