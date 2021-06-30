$(document).ready(function() {
  var $lg = $("#aniimated-thumbnials");
  $lg
    .justifiedGallery({
      border: 6
    })
    .on("jg.complete", function() {
      $lg.lightGallery({
        pager: true
      });
    });
});