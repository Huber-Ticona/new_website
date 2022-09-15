//CAMBIO DE IMAGENES MEDIANTE CLICK
$('.producto-imagenes img').click(function(e){
    let img_src = e.target.src
    $('.imagen').attr('src',img_src)
})

