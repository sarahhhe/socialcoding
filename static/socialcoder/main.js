var $rows = $("tr");
$("#search").keyup(function() {
  var val = $.trim(this.value);
  if (val === "")
      $rows.show();
  else {
      $rows.hide();
      $rows.has("td:contains(" + val + ")").show();
  }
});

$("#cmtbtn").on("click", function(){
  $.ajax ({
    url : "addcomment/",
    method : "POST",
    data : $("#cmtform").serializeArray(),
    success : function (data) {
    }
  })
})

$(document).ready(function(){
  $(".upvote").click(function(){
    var id = this.id
    url="upvote/"
    vote = 1
    $.ajax({
      url: url+id,
      type: 'PUT',
      data : {'votes' : vote},
      success: function(data) {
         }
      })
  });
});

$(document).ready(function(){
  $(".upvote-feed").on("click", function(){
    var id = this.id
    url1="post/"
    url2="upvote/"
    vote = 1
    $.ajax({
      url: url1+id+"/"+url2+id,
      type: 'PUT',
      data : {'votes' : vote},
      success: function(data) {
         }
      })
  });
});

  $(".downvote").on("click", function(){
    var id = this.id
    url="downvote/"
    vote = 1
    $.ajax({
      url: url+id,
      type: 'PUT',
      data : {'votes' : vote},
      success: function(data) {
         }
      })
  });

  $(document).ready(function(){
    $(".downvote-feed").on("click", function(){
      var id = this.id
      url1="post/"
      url2="downvote/"
      vote = 1
      $.ajax({
        url: url1+id+"/"+url2+id,
        type: 'PUT',
        data : {'votes' : vote},
        success: function(data) {
           }
        })
    });
  });
