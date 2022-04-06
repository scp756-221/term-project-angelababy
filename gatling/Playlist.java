
package computerdatabase;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import java.time.Duration;

public class Playlist extends Simulation {

  HttpProtocolBuilder httpProtocol =
      http
          // Here is the root for all relative URLs
          .baseUrl("http://")
          // Here are the headers
          .acceptHeader("text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
          .doNotTrackHeader("1")
          .acceptLanguageHeader("en-US,en;q=0.5")
          .acceptEncodingHeader("gzip, deflate")
          .header("Authorization","auth")
          .userAgentHeader(
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20100101 Firefox/16.0");

  ScenarioBuilder scn =
      scenario("Test Playlist Service")
          .exec(http("create_playlist")
            .post("/")
            .body(StringBody("{\"PlayListName\": \"newList\",\"Songs\":\"[The Last Great American Dynasty,Reliever]\"}"))
            .check(jsonPath("$playlist_id").saveAs("playlist_id")))
          .pause(5)
          .exec(http("get_playlist").get("?playlist_id=${playlist_id}"))
          .pause(5)
          .exec(http("add_song_to_playlist")
            .put("/add_song_to_list?playlist_id=${playlist_id}")
            .body(StringBody("{\"music_id\":\"6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea\"}"))
             )
          .pause(5)
          .exec(http("delete_song_from_playlist")
            .put("/delete_song_from_list?playlist_id=${playlist_id}")
            .body(StringBody("{\"music_id\":\"6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea\"}"))
               )
          .pause(5)
          .exec(http("delete_playlist").delete("?playlist_id=${playlist_id}"));
          

  {
    setUp(scn.injectOpen(atOnceUsers(10)).protocols(httpProtocol));
  }
}
