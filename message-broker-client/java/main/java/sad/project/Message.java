package sad.project;

import lombok.*;

import java.time.LocalDateTime;

@AllArgsConstructor
@Builder
@Getter
@Setter
@ToString
public class Message {
    private String key;
    private String value;
    private LocalDateTime time_arrived; // It is the arriving time of the message
}