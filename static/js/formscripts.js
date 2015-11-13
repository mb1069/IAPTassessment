function readURL(input){
    window.previousImage = $('#preview-image').attr('src');
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e){
            $('#preview-image').attr('src', e.target.result)
                .width(100)
                .height(133);
        };
        reader.readAsDataURL(input.files[0]);
    }
}



function addToList(select, value){
    if (value!= '' && value != undefined && $(select).find('option[value=\''+value+'\']').length==0){
        $(select).append($("<option></option>")
            .attr('value', value)
            .text(value));
    }
}

function selectAll(){
    $('#artists').find('option:not(:selected)').selected=true;
    $('#writers').find('option:not(:selected)').selected=true;
}
