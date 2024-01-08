package sad.project;

import lombok.*;

import java.time.LocalDateTime;

@AllArgsConstructor
@Getter
@Setter
@ToString
public class Message {
    private String data; // It is the main data of the message to be transferred
    private LocalDateTime time_arrived; // It is the arriving time of the message

    @Override
    public String toString() {
        return "Message{" + "data='" + this.data + "'" + ", time_arrived='" + this.time_arrived + "'}";
    }
}