<!DOCTYPE HTML>
<html>
  <head>
    <link rel="stylesheet" href="css/stylesheet.css"></script>
  </head>
  <body>
    <h1>Online Video Downloader</h1>
    <form action="/download" method="post">
      URL<br/>
      <input name="url" type="text" /><br/><br/>
      Destination<br/>
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
