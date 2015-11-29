function deleteComic(id, comicbook_name, url){
    if (confirm("Are you sure you would like to delete "+comicbook_name + "?")){
        $.ajax({
            url: url,
            type: 'post',
            data: {'comicbookid': id},
            success: function(response){
                console.log("SUCCESS");
                $("#"+id).hide('slow', function(){$("#"+id).remove();});
            }
        });
    }
}