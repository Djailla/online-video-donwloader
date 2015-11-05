<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Home page of the NAS OS Online Video Download</title>
    <link rel="stylesheet" href="css/stylesheet.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>
    <link rel="stylesheet" href="css/tooltip.css">
    <script>
      $(function() {
        $( document ).tooltip({
          position: {
            my: "center bottom-20",
            at: "center top",
          }
        });
      });
    </script>
  </head>
  <body>
    <h1>Online Video Downloader</h1>
    <form action="/download" method="post">
      <h2>URL</h2>
      <input name="url" type="text" title="Please copy here the URL of the video to download."/><br/><br/>
      <h2>Destination</h2>
      <select name="dest_path">
        {{!path_list}}!
      </select>
      <br/><br/>
      <input class="btn" value="Download" type="submit" />
    </form>
    <br>
    <p style="font-size: 20px;"><a href="https://rg3.github.io/youtube-dl/supportedsites.html" target="_blank">Supported sites</a><p>
  </body>
</html>
