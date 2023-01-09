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
  window.location.href = "/producto/"+ alt
})

$(document).ready(function(){
  console.log('pagina cargada')
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
});
