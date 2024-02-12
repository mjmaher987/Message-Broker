package sad.project;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.function.Function;

public class Consumer {
    private final static String PULL_URL = "http://0.0.0.0:8000/pull/";

    public Message pull() {
        Message message = null;
        try {
            URL url = new URL(PULL_URL);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");

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

            if (response.toString().isEmpty()) {
                return null;
            }
            message = gson.fromJson(response.toString(), Message.class);

            connection.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return message;
    }

    public <T> void subscribe(Function<Message, T> function, long intervalMillis) {
        Thread subscriberThread = getSubscriberThread(function, intervalMillis);
        subscriberThread.start();
    }


    private <T> Thread getSubscriberThread(final Function<Message, T> function, final long intervalMillis) {
        return new Thread(() -> {
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
    }
}