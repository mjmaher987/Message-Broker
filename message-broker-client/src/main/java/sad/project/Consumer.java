package sad.project;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class Consumer {
    public Message pull() {
        Message message = null;
        try {
            // Create a URL object with the API endpoint
            URL url = new URL("https://jsonplaceholder.typicode.com/posts/1");

            // Create a HttpURLConnection object
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            // Set the request method to GET
            connection.setRequestMethod("GET");

            // Get the response code
            int responseCode = connection.getResponseCode();
            System.out.println("Response Code: " + responseCode);

            // Read the response from the API
            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String inputLine;
            while ((inputLine = reader.readLine()) != null) {
                response.append(inputLine);
            }
            reader.close();

            // Parse JSON response into MyObject using Gson
            Gson gson = new GsonBuilder().create();
            message = gson.fromJson(response.toString(), Message.class);

            // Print the object
            System.out.println("Received Object:");
            System.out.println("key: " + message.getKey());
            System.out.println("value: " + message.getKey());

            // Close the connection
            connection.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return message;
    }
}