package sad.project;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class Producer {
    private final static String PUSH_URL = "http://localhost:8000/push";

    public void push(Message message) {
        try {
            Gson gson = new GsonBuilder().create();
            String jsonBody = gson.toJson(message);

            URL url = new URL(PUSH_URL);

            HttpURLConnection connection = getPostConnection(url);

            try (DataOutputStream wr = new DataOutputStream(connection.getOutputStream())) {
                wr.write(jsonBody.getBytes());
            }

            int responseCode = connection.getResponseCode();
            System.out.println("Response Code: " + responseCode);

            String response = getResponse(responseCode, connection);
            System.out.println(response);

            connection.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static String getResponse(final int responseCode, final HttpURLConnection connection) throws IOException {
        BufferedReader reader;
        if (responseCode == HttpURLConnection.HTTP_OK) {
            reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        } else {
            reader = new BufferedReader(new InputStreamReader(connection.getErrorStream()));
        }

        StringBuilder response = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            response.append(line);
        }
        reader.close();
        return response.toString();
    }

    private static HttpURLConnection getPostConnection(final URL url) throws IOException {
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setRequestProperty("Accept", "application/json");
        connection.setDoOutput(true);
        return connection;
    }
}
