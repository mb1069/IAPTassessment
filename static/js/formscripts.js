function readURL(input){
    console.log(111);
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e){
            $('#preview-image').attr('src', e.target.result)
                .width(100)
                .height(130);
        };
        reader.readAsDataURL(input.files[0])
    }
}
