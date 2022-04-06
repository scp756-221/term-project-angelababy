package computerdatabase;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import java.time.Duration;

public class User extends Simulation {

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
      scenario("Test User Service")
          .exec(http("create_user")
            .post("/")
            .body(StringBody("{\"lname\":\"Ma\",\"email\":\"jackma@gmail.com\", \"fname\":\"Jack\"}"))
            .check(jsonPath("$user_id").saveAs("user_id")))
          .pause(5)
          .exec(http("get_user").get("?user_id=${user_id}"))
          .pause(5)
          .exec(http("update_user")
            .put("?user_id=${user_id}")
            .body(StringBody("{\"lname\":\"Li\",\"email\":\"jasonli@gmail.com\", \"fname\":\"Jason\"}"))
             )
          .pause(5)
          .exec(http("delete_user")
            .delete("?user_id=${user_id}"));
             
          
          

  {
    setUp(scn.injectOpen(atOnceUsers(10)).protocols(httpProtocol));
  }
}
