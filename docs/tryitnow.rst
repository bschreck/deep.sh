Try It Now!
===========
Try out deepsh right here in the browser. Just press the "Run This"
button below!

.. raw:: html

    <div id="tryitnow"></div>
    <script>
      var app = Elm.Main.init({
        node: document.getElementById('tryitnow'),
          flags: {
            placeholder: "<img src=\"_static/better_colors_windows.png\">",
            serverUrl: "https://runthis.deepsh.org:80",
        }
      });
    </script>
