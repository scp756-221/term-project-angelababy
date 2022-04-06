package computerdatabase;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import java.time.Duration;

public class Music extends Simulation {

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
      scenario("Test Music Service")
          .exec(http("create_song")
            .post("/")
            .body(StringBody("{\"Artist\":\"James\",\"SongTitle\":\"Song\"}"))
            .check(jsonPath("$music_id").saveAs("music_id")))
          .pause(5)
          .exec(http("get_song").get("?music_id=${music_id}"))
          .pause(5)
          .exec(http("list_all")
            .get("/"))
          .pause(5)
          .exec(http("delete_song")
            .delete("?music_id=${music_id}"));
             
          
          

  {
    setUp(scn.injectOpen(atOnceUsers(10)).protocols(httpProtocol));
  }
}
