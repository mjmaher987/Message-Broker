package sad.project;

import java.time.LocalDateTime;
import java.util.concurrent.BlockingQueue;

public class Producer implements Runnable {
    private final BlockingQueue<Message> queue;

    public Producer(BlockingQueue<Message> queue) {
        this.queue = queue;
    }

    @Override
    public void run() {
        try {
            while (true) {
                Message message = createMessage();
                queue.put(message);
                Thread.sleep(1000);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private Message createMessage() {
//        It depends on the server
        String data = "Hello from the Producer!";
        LocalDateTime timeArrived = LocalDateTime.now();
        return new Message(data, timeArrived);
    }
}
