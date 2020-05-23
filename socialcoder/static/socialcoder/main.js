$(".acceptResponse").on("click", function(){
  console.log("accept response as best")
  var id = this.id
  console.log(id)
  url="accept/"
  $.ajax({
    url: url+id,
    type: 'PUT',
    success: function(data) {
       }
    })
  location.reload();
});

$(function () {
    $(window).on('scroll', function () {
        if ( $(window).scrollTop() > 10 ) {
            $('.navbar').addClass('active');
        } else {
            $('.navbar').removeClass('active');
        }
    });
});


$(".followCategory").on("click", function(){
  var id = this.id
  url="followCategory/"
  $.ajax({
    url: url+id,
    type: 'PUT',
    success: function(data) {
       }
    })
  location.reload();
});

function filterSelection(c) {
  var x, i, t;
  t = document.getElementsByClassName("leaderboardTitle");
  t[0].innerHTML = "Today's Top socialCoders in "+c // change the leaderboard title
  x = document.getElementsByClassName("filterDiv");
  if (c == "all") c = "";
  for (i = 0; i < x.length; i++) {
    removeClass(x[i], "show"); // remove all scores
    if (x[i].className.indexOf(c) > -1) addClass(x[i], "show");
  }
}

function addClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {element.className += " " + arr2[i];}
  }
}

function removeClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);
    }
  }
  element.className = arr1.join(" ");
}

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

$('#username-search-input').autocomplete({
  source: function(request, response) {
    $.ajax({
      url: 'usernames',
      success: function(data) {
        response($.ui.autocomplete.filter(data.usernames, request.term));
       }
     });
   },
  minLength: 0
})

function upvoteResponse(responseid, postid) {
  url1="post/"
  url3="upvote/response/"
  vote = 1
  $.ajax({
    url: url1+postid+"/"+url3+responseid,
    type: 'PUT',
    data : {'response_votes' : vote},
    success: function(data) {
       }
    })
  location.reload();
}

function downvoteResponse(responseid, postid) {
  url1="post/"
  url3="downvote/response/"
  vote = 1
  $.ajax({
    url: url1+postid+"/"+url3+responseid,
    type: 'PUT',
    data : {'response_votes' : vote},
    success: function(data) {
       }
    })
  location.reload();
}



$(".upvote").on("click", function(){
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
  location.reload();
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
    location.reload();
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
    location.reload();
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
      location.reload();
    });
  });
