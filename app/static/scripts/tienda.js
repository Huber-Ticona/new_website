$(".open-sidebar-categoria").on("click", function () {
  $(".tienda_sidebar").addClass("active");
});

$(".close-sidebar-categoria").on("click", function () {
  $(".tienda_sidebar").removeClass("active");
});
$(".tienda_sidebar_relleno").on("click", function () {
  $(".tienda_sidebar").removeClass("active");
});
/* para movil */
function abrir_categorias() {
  if ($(".cont_categorias").is(":hidden")) {
    $(".cont_categorias").slideDown("fast");
  } else {
    $(".cont_categorias").slideUp("fast");
  }
}
function abrir_precios() {
  if ($(".cont_precios").is(":hidden")) {
    $(".cont_precios").slideDown("fast");
  } else {
    $(".cont_precios").slideUp("fast");
  }
}
/* para pc */

$("#card-contenido img").on("click", function (e) {
  alt = e.target.alt;
  //window.location.href = "producto/"+ alt
  //$.get("producto/"+ alt)
  console.log(window.location);
});

// collapse fix
// Controlador del evento click para los botones que ocultan los elementos colapsables
document.querySelectorAll('[data-toggle="collapse"]').forEach(function (btn) {
  btn.addEventListener("click", function (event) {
    event.preventDefault(); // Detener la propagación del evento click
    // Resto de la lógica para mostrar/ocultar los elementos colapsables
  });
});

var f = [0, 0];
var g = [0, 0];
$(document).ready(function () {
  if ($("#input-slider-range-md")[0]) {
    var c = document.getElementById("input-slider-range-md"),
      d = document.getElementById("input-slider-range-md-value-low"),
      e = document.getElementById("input-slider-range-md-value-high");
    f = [d, e];
    noUiSlider.create(c, {
      start: [
        parseInt(d.getAttribute("data-range-value-low")),
        parseInt(e.getAttribute("data-range-value-high")),
      ],
      connect: !0,
      range: {
        min: parseInt(c.getAttribute("data-range-value-min")),
        max: parseInt(c.getAttribute("data-range-value-max")),
      },
    }),
      c.noUiSlider.on("update", function (a, b) {
        //SINCRONIZA SLIDER MD y LG
        $("#input-slider-range-md-min").val(a);
        $("#input-slider-range-md-max").val(b);
        console.log(a);
        console.log(b);
        g[b].textContent = a[b];
        f[b].textContent = a[b];
      });
  }
  if ($("#input-slider-range-lg")[0]) {
    var c = document.getElementById("input-slider-range-lg"),
      d = document.getElementById("input-slider-range-lg-value-low"),
      e = document.getElementById("input-slider-range-lg-value-high");
    g = [d, e];
    noUiSlider.create(c, {
      start: [
        parseInt(d.getAttribute("data-range-value-low")),
        parseInt(e.getAttribute("data-range-value-high")),
      ],
      connect: !0,
      range: {
        min: parseInt(c.getAttribute("data-range-value-min")),
        max: parseInt(c.getAttribute("data-range-value-max")),
      },
    }),
      c.noUiSlider.on("update", function (a, b) {
        //SINCRONIZA SLIDER MD y LG
        $("#input-slider-range-lg-min").val(parseInt(a[0]));
        $("#input-slider-range-lg-max").val(parseInt(a[1]));
        g[b].textContent = a[b];
        f[b].textContent = a[b];
      });
  }

  $(".tienda_carrusel").owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    navText: [
      '<svg width="50" height="50" viewBox="0 0 24 24"><path d="M16.67 0l2.83 2.829-9.339 9.175 9.339 9.167-2.83 2.829-12.17-11.996z"/></svg>',
      '<svg width="50" height="50" viewBox="0 0 24 24"><path d="M5 3l3.057-3 11.943 12-11.943 12-3.057-3 9-9z"/></svg>',
    ],
    responsive: {
      0: {
        items: 1,
      },
      600: {
        items: 3,
      },
      1000: {
        items: 5,
      },
    },
    dots: true,
  });
});
