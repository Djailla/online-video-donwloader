<!DOCTYPE HTML>
<html>
  <head>
    <link rel="stylesheet" href="css/stylesheet.css"></script>
  </head>
  <body>
    <h1>Web Video Downloader</h1>
    <form action="/download" method="post">
      URL<br/>
      <input name="url" type="text" /><br/><br/>
      Destination<br/>
      <input name="dest_path" type="text" value="{{default_path}}"/><br/><br/>

      <input class="btn" value="Download" type="submit" />
    </form>
  </body>
</html>
