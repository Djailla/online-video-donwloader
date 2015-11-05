<!DOCTYPE HTML>
<html>
  <head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
    <script src="js/jquery.percentageloader-0.1.min.js"></script>
    <link rel="stylesheet" href="css/stylesheet.css"></script>
    <link rel="stylesheet" href="css/progress.css"></script>
  </head>
  <body>
    <div id="container">
      <div id="topLoader">
      </div>
      <a class="btn" href="/cancel">Cancel</a>
      <script>
        $(function() {
          var $topLoader = $("#topLoader").percentageLoader({
            width: 256,
            height: 256,
            controllable: true,
            progress: 0.5,
            onProgressUpdate: function(val) {
              $topLoader.setValue(Math.round(val * 100.0));
            }
          });

          topLoaderRunning = true;
          $topLoader.setProgress(0);
          $topLoader.setValue('');
          var progress = 0;
          var speed = 0;

          var animateFunc = function() {
            $.get('/progress', function(result){
              progress = result.progress;
              speed = result.speed;
            }, 'json');

            $topLoader.setProgress(progress/100);
            $topLoader.setValue(speed);

            if (progress == -1) {
              window.location = "/dl_error";
            }
            else if (progress < 100) {
              setTimeout(animateFunc, 500);
            } else {
              window.location = "/complete";
            }
          }
          setTimeout(animateFunc, 500);
        });
      </script>
    </div>
  </body>
</html>
