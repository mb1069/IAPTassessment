function deleteComic(id, comicbook_name, url, myComicsURL){
    if (confirm("Are you sure you would like to delete "+comicbook_name + "?")){
        $.ajax({
            url: url,
            type: 'post',
            data: {'comicbookid': id},
            success: function(response){
                console.log("SUCCESS");
                var div = $("#" + id);
                if (div.length>0) {
                    div.hide('slow', function () {
                        div.remove();
                    });
                } else {
                    window.location.href = myComicsURL;
                }
            }
        });
    }
}