// <!--Exam candidate number: Y0076159-->

/**
 * Quick js method to delete a comic using comics.comicdelete()
 * @param id: id of comicbook to delete
 * @param comicbook_name: name of comicbook to delete, for prompt message
 * @param url: url for ajax
 * @param myComicsURL: return url to redirect
 */
function deleteComic(id, comicbook_name, url, myComicsURL){
    if (confirm("Are you sure you would like to delete "+comicbook_name + "?")){
        $.ajax({
            url: url,
            type: 'post',
            data: {'comicbookid': id},
            success: function(response){
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
