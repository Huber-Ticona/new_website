$('.open-sidebar-categoria').on('click', function(){
  $('.tienda_sidebar').addClass('active')
})

$('.close-sidebar-categoria').on('click', function(){
  $('.tienda_sidebar').removeClass('active')
})
$('.tienda_sidebar_relleno').on('click', function(){
  $('.tienda_sidebar').removeClass('active')
})
/* para movil */
function abrir_categorias (){
  if ( $('.cont_categorias').is(":hidden")) {
      $('.cont_categorias').slideDown("fast");
      
  }else {
      $('.cont_categorias').slideUp("fast");
  }
}
function abrir_precios(){
  if ( $('.cont_precios').is(":hidden")) {
      $('.cont_precios').slideDown("fast");
  }else {
      $('.cont_precios').slideUp("fast");
  }
}
/* para pc */

$('#card-contenido img').on('click',function(e){
  alt = e.target.alt
  //window.location.href = "producto/"+ alt
  //$.get("producto/"+ alt)
  console.log(window.location)
  
})

$(document).ready(function(){
  var slider_sm = document.getElementById('slider_filtro_movil');
  var slider_lg = document.getElementById('slider_filtro_escritorio');
  noUiSlider.create(slider_sm, {
    start: [20, 80],
    range: {
      'min': 0,
      'max': 100
    }
  });
  noUiSlider.create(slider_lg, {
    start: [20, 80],
    range: {
      'min': 0,
      'max': 100
    }
  });
  
  $('.tienda_carrusel').owlCarousel({
    loop:true,
    margin:10,
    nav: true,
    navText: [
      '<svg width="50" height="50" viewBox="0 0 24 24"><path d="M16.67 0l2.83 2.829-9.339 9.175 9.339 9.167-2.83 2.829-12.17-11.996z"/></svg>',
      '<svg width="50" height="50" viewBox="0 0 24 24"><path d="M5 3l3.057-3 11.943 12-11.943 12-3.057-3 9-9z"/></svg>'
    ],
    responsive:{
        0:{
            items:1
        },
        600:{
            items:3
        },
        1000:{
            items:5
        }
    },
    dots:true
  });

  
});


  