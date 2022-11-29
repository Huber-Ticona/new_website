var aux_sidebar_cola = [] // DETERMINA SI VOLVER AL SIDEBAR PRINCIPAL O AL NEXT_SIDEBAR POR ID
var aux_sidebar_id = 0
var next = 1
var switch_slide_pc = false
$('.open-sidebar').on('click', function(){
    $('.principal_sidebar').addClass('active')
  })
// CERRAR SIDEBAR PRINCIPAL -> VOLVER PRINCIPAL CONTENIDO
$('.principal_sidebar').on('click','.close-sidebar', function(){
  next = 1 // para volver a navegar desde categoria nivel 1
  $('.sidebar').css('margin-left','0' ) 
  
  $('.principal_sidebar').removeClass('active')
  console.log('cerrando sidebar principal')
})

// ABRIR NEXT SLIDE
$('.open_next_sidebar').on('click', function(){
  
    $('.sidebar').css('margin-left','-100%' ) 
    $('#side_'+ next.toString()).empty()
    let y = $('.view_1').html();// nivel de categoria 1 = TIENDA
    $('#side_'+ next.toString()).append(y)
    

  //
  //let z = '</div>'
  /*let x = '<div class="next_sidebar" id="side_'+ next.toString() +'">'
  let y = $('.view_1').html();
  let z = '</div>'
  
  aux_sidebar_id = 1
  $('.principal_sidebar').append(x+y+z);
  //console.log('viendo next',copia)*/
})

// MOVER NEXT_SLIDE  CATEGORIA ANTERIOR
$('.next_sidebar').on('click', '.close_next_sidebar', function(){
  console.log('next',next)
    if(next - 1 == 0){
      console.log('volver al sidebar')
      $('.sidebar').css('margin-left','0' )
      
    }else{
      next = next - 1
      $('#side_' + next.toString() ).css('margin-left','0' )
      console.log('volver al slide',next)
    }
})

  //MOVER NEXT_SLIDE  CATEGORIA SIGUIENTE
$('.next_sidebar').on('click', '.categoria_link', function(){
  if(next < 3){
    console.log('moviendo side ',next)
    let aux = next
    next = next + 1

    console.log(this.id)
    console.log(typeof(this.id)) //data -> 1: ver categoria / 2: volver de categoria
    let id = parseInt(this.id)
    console.log('ver categoria' , id)

    if( $('.view_' + id).length ){ // VERIFICA SI EXISTE EL DIV
      console.log('existe div')
      var copia = $('.view_' + id).html();
      //console.log(copia)
      $('#side_' + next.toString() ).empty()
      $('#side_' + next.toString() ).append(copia)
      $('#side_' + aux.toString() ).css('margin-left','-100%' ) 
    }else{
      console.log('no existe div')
    }
  }else{
      console.log('no se permite mas desplazamiento')
    }
})

$('.slide_categorias').on('click', '.categoria_link',function(){
console.log('navegando categorias PC')
if(switch_slide_pc != true){
  console.log(this.id)
    console.log(typeof(this.id)) //data -> 1: ver categoria / 2: volver de categoria
    let id = parseInt(this.id)
    console.log('ver categoria' , id)

    if( $('.view_' + id).length ){ // VERIFICA SI EXISTE EL DIV
      console.log('existe div')
      var copia = $('.view_' + id).html();
      //console.log(copia)
      $('.slide_categorias').empty()
      $('.slide_categorias' ).append(copia)
      switch_slide_pc = true // indica no mostrar categorias formato lvl 3

    }else{
      console.log('no existe div')
    }
}else{
  console.log('no se permite mostrar mas niveles')
}
})
$('.slide_categorias').on('click', '.inicio_slide_categorias',function(){
  let y = $('.view_1').html();// nivel de categoria 1 = TIENDA
  switch_slide_pc = false
  $('.slide_categorias').empty()
  $('.slide_categorias').append(y)
})

$('nav').on('click','.visualizar_categorias_lg',function(){
  console.log('test view')
  if($('.slide_categorias').css('display') == 'block'){ 
    
    
    $('.slide_categorias').hide('fast')
    //$('#contenido_0').css('display','block')
  } else { 
    let y = $('.view_1').html();// nivel de categoria 1 = TIENDA
    $('.slide_categorias').empty()
    $('.slide_categorias').append(y)
    $('.slide_categorias').show('fast') 
    //$('#contenido_0').css('display','none')
  }
})

//