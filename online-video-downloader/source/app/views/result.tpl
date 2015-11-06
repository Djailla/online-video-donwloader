<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="css/stylesheet.css">
  </head>
  <body>
    <h1>{{title}}</h1>
    % if subtitle != '':
    <h2>{{subtitle}}</h2>
    <h3>in</h3>
    <h2>{{dest_path}}</h2>
    % end
    <a class="btn" href="/">Ok</a>
  </body>
</html>
