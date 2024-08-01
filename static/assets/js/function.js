const monthNames = [
  "Jan",
  "Feb",
  "Mar",
  "April",
  "May",
  "June",
  "July",
  "Aug",
  "Sept",
  "Oct",
  "Nov",
  "Dec",
];

$("#commentForm").submit(function (e) {
  e.preventDefault();

  let dt = new Date();
  let time =
    dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear();

  $.ajax({
    data: $(this).serialize(),

    method: $(this).attr("method"),

    url: $(this).attr("action"),

    dataType: "json",

    success: function (res) {
      console.log("Comment Saved to DB...");

      if (res.bool == true) {
        $("#review-res").html("Review added successfully.");
        $(".hide-comment-form").hide();
        $(".add-review").hide();

        let _html =
          '<div class="single-comment justify-content-between d-flex mb-30">';
        _html += '<div class="user justify-content-between d-flex">';
        _html += '<div class="thumb text-center">';
        _html +=
          '<img src="https://thumbs.dreamstime.com/b/default-avatar-profile-vector-user-profile-default-avatar-profile-vector-user-profile-profile-179376714.jpg" alt="" />';
        _html +=
          '<a href="#" class="font-heading text-brand">' +
          res.context.user +
          "</a>";
        _html += "</div>";

        _html += '<div class="desc">';
        _html += '<div class="d-flex justify-content-between mb-10">';
        _html += '<div class="d-flex align-items-center">';
        _html += '<span class="font-xs text-muted">' + time + " </span>";
        _html += "</div>";

        for (var i = 1; i <= res.context.rating; i++) {
          _html += '<i class="fas fa-star text-warning"></i>';
        }

        _html += "</div>";
        _html += '<p class="mb-10">' + res.context.review + "</p>";

        _html += "</div>";
        _html += "</div>";
        _html += " </div>";

        $(".comment-list").prepend(_html);
      }
    },
  });
});

$(document).ready(function () {
  $(".loader").hide();

  $(".filter-checkbox").on("click", function () {
    let filter_object = {};

    $(".filter-checkbox").each(function (index) {
      let filter_value = $(this).val();
      let filter_key = $(this).data("filter");

      console.log(filter_value, filter_key);

      filter_object[filter_key] = Array.from(
        document.querySelectorAll(
          "input[data-filter=" + filter_key + "]:checked"
        )
      ).map(function (element) {
        return element.value;
      });
    });
    $.ajax({
      url: "/filter-product",
      data: filter_object,
      dataType: "json",
      beforeSend: function () {
        $(".loader").show();
      },
      success: function (res) {
        $("#filtered-product").html(res.data);

        console.log(res);
        $(".loader").show();
      },
    });
  });
});

$("#add-to-cart-btn").on("click", function () {
  let quantity = $("#product-quantity").val();
  let product_title = $(".product-title").val();
  let product_id = $(".product-id").val();
  let product_price = $(".current-product-price").text();
  let this_val = $(this);
  console.log("Quantity:", quantity);
  console.log("Id:", product_id);
  console.log("Title:", product_title);
  console.log("Price:", product_price);
  console.log("This is:", this_val);
  $.ajax({
    url: "/add-to-cart",
    data: {
      id: product_id,
      qty: quantity,
      title: product_title,
      price: product_price,
    },
    dataType: "json",
    beforeSend: function () {
      this_val.html("Added To Cart");
    },
    success: function (response) {
      console.log(response);
      $(".cart-items-count").text(response.totalcartitems);
      this_val.attr("disabled", false);
    },
  });
});
