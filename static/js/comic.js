function deleteComic(id, comicbook_name, url, myComicsURL){
    if (confirm("Are you sure you would like to delete "+comicbook_name + "?")){
        $.ajax({
            url: url,
            type: 'post',
            data: {'comicbookid': id},
            success: function(response){
                console.log("SUCCESS");
                if ($("#"+id).length>0) {
                    $("#" + id).hide('slow', function () {
                        $("#" + id).remove();
                    });
                } else {
                    window.location.href = myComicsURL;
                }
            }
        });
    }
}