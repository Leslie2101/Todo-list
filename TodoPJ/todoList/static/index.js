const deleteNote = (noteId) => {
    fetch("/delete-note",{
        method: "POST",
        body: JSON.stringify({note_id: noteId})
    }).then( (response) => {
    window.location.href="/home";
    })
}

function checkedstate(noteId){

    fetch('/complete',{
        method: "POST",
        body: JSON.stringify({note_id: noteId})
    }).then( (response) => {
        window.location.href="/home";
    })

}
function edit_todo(id){
    $("#titleInput").val($("#title_" + id).text());
    $("#submit").text("Update");
    addCancelButton();

}

function resetingButton(){
    document.getElementById("todo-form").reset();
    $("#submit").text("Add Todo");
    $("#cancelButton").remove();
}

function addCancelButton(){
    var cancelbutton = document.createElement("button");
    cancelbutton.type= null;
    cancelbutton.id = "cancelButton";
    cancelbutton.className= "mx-auto btn btn-primary";
    cancelbutton.style.backgroundColor="orange";
    cancelbutton.innerText= "Cancel";
    cancelbutton.addEventListener('click', function(){resetingButton()});
    document.getElementById("buttons").appendChild(cancelbutton);    
}



