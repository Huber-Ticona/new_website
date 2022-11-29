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
/* slider precio */
window.addEventListener('range-changed', 
(e) => {console.log(`Range changed for: ${e.detail.sliderId}. Min/Max range values are available in this object too`)})
