// The service box
const dragDropArea = document.getElementById('drag-drop-area');
// The file that a user is going to drop/select in the service box
const input = dragDropArea.querySelector('#fileElem');
// The text displayed inside the service box before the ttl has been generated (name of the file selected or instructions for the user)
const inputName = dragDropArea.querySelector('#drag-text');
// Submit button
const submitButton = document.getElementById('submit');
// Download button
const downloadButton = document.getElementById('download');
// The text displayed inside the service box after the ttl has been generated
const responseText = document.getElementById('response');
// Type selection
const typeSelected = document.getElementById('type-selected');
// Flatten selection
const flattenSelected = document.getElementById('flatten-selected');

// Error/warning sections
const errorReport = document.getElementById('error-report');
const warningReport = document.getElementById('warning-report');

//Warning accordions
const baseItem = document.getElementById('base-item');
const baseBody = document.getElementById('base-body');

//Error accordions
const conceptsItem = document.getElementById('concepts-item');
const conceptsBody = document.getElementById('concepts-body');

let response;
let file;
let loadFile = false;
let loadTransformedDiagram = false;
let loadType = false;
let loadFlatten = false;

//Drag enter event handler
//If the drag file enter the box => the box color is white and
//it is detected as a new file
dragDropArea.addEventListener('dragenter', (e) => {
    e.preventDefault();
    loadFile = false;
    submitButton.disabled = true;
    responseText.style.display = 'none';
    inputName.style.display = 'block';
    dragDropArea.style.backgroundColor = 'white';
    inputName.innerHTML = 'Drag and drop your diagram or click to choose your file';
});

//Drag leave event handler
//If the drag file leave the box => the box color is white
dragDropArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dragDropArea.style.backgroundColor = 'white';
    inputName.innerHTML = 'Drag and drop your diagram or click to choose your file';
});

//Drag over event handler
//While the drag file is on the box => the box color is grey
dragDropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dragDropArea.style.backgroundColor = '#ECECEC';
    inputName.innerHTML = 'Release your diagram';
});

//Mouseover event handler
//While the mouse is on the box => the mouse pointer change in
//order to indicate to the user that they can click the box
dragDropArea.addEventListener('mouseover', ()=>{
    dragDropArea.style.cursor = 'pointer';
});

//Click event handler
//If the user click on the box => the user can select a local file to upload
dragDropArea.addEventListener('click', (e)=>{
    // Erase the file path in order to trigger the change event when selecting a file with the same path
    input.value = null;
    input.click();
});

//Change event handler
//Each time a user select a file => indicate to the user the name of the file
input.addEventListener('change', (e) => {
    loadFile = false;
    submitButton.disabled = true;
    responseText.style.display = 'none';
    inputName.innerHTML = 'Drag and drop your diagram or click to choose your file';
    inputName.style.display = 'block';
    checkFiles(input.files);
});

//Drop event handler
//Each time a user drop a file => indicate to the user the name of the file
dragDropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dragDropArea.style.backgroundColor = 'white';
    inputName.innerHTML = 'Drag and drop your diagram or click to choose your file';
    checkFiles(e.dataTransfer.files);
});

//Function to check the number of files
function checkFiles(files){
    if (files.length === undefined) {
        //There is just one file
        processFile(files);
    } else if (files.length === 1) {
        //There is just one file
        processFile(files[0]);
    } else {
        //There is more than one file. Just the first file will be processed
        alert('Only the first file is going to be processed');
        processFile(files[0]);
    }
}

//Function to show the name of the diagram the user selected, check its extension
//and load the file in memory
function processFile(f){
    if (f != undefined && (f.type == 'text/csv' || f.type == 'application/x-zip-compressed')){
        //File extension correct'
        inputName.innerHTML = '<b>"' + f.name + '"</b>' + ' selected';
        file = f;
        loadFile = true;
        enableSubmitButton();
    } else {
        alert('The extension of the file must be csv or zip');
    }
}

//Click event handler for the button 'submit'
//If there is not a file loaded => warn the user
//If there is a file loaded => transform the diagram
submitButton.addEventListener('click', (e) => {
    //Submit
    if (loadFlatten && loadType && loadFile){
        //Correct submit
        loadFile = false;
        submitButton.disabled = true;
        inputName.innerHTML = 'Detecting your patterns';
        detectPattern(file, typeSelected.value, flattenSelected.value);
    } else {
        //Incorrect submit
        alert('A file has not been selected');
    }
});

//Change event handler
//Each time a user select a pattern type => check if the submit button can be enable
typeSelected.addEventListener('change', (e) => {
    if (typeSelected.value){
        loadType = true;
        enableSubmitButton();
    }
    else{
        loadType = false;
        submitButton.disabled = true;
    }
});

//Change event handler
//Each time a user select a pattern type => check if the submit button can be enable
flattenSelected.addEventListener('change', (e) => {
    if (flattenSelected.value){
        loadFlatten = true;
        enableSubmitButton();
    }
    else{
        loadFlatten = false;
        submitButton.disabled = true;
    } 
});

// The submit button is enabled when the user has selected:
//  - A pattern type (through the selection)
//  - If the collections are going to be flatten (through the selection)
//  - The file (through the drag and drop)
function enableSubmitButton(){

    if (loadFlatten && loadType && loadFile){
        submitButton.disabled = false;
    }
    else{
        submitButton.disabled = true;
    }
}

// Function to make the HTTP Post request to the Chowlk API
function detectPattern(file, typeValue, flattenValue){
    loadTransformedDiagram = false;
    downloadButton.disabled = true;
    //const uri = 'https://chowlk.linkeddata.es/api';
    const uri = 'http://localhost:5000/api';
    // Create an HTTP request
    const xhr = new XMLHttpRequest();
    // Specify how the data is going to be sent in the request
    const fd = new FormData();
    // Set the type of the request (Post)
    xhr.open('POST', uri);
    // When the response is received the following function is going to be executed
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status == 200){
            //Diagram transformed
            response = xhr.responseText;
            
            errorReport.style.display = 'none';
            warningReport.style.display = 'none';
            
            inputName.style.display = 'none';
            responseText.style.display = 'block';
            responseText.innerText = "Please click the button below to download the files";
            loadTransformedDiagram = true;
            downloadButton.disabled = false;


        }    
    }
    if (file.type == 'text/csv'){
        // Append the file (CSV)
        fd.append('ontologiesCsv', file);
    }
    else if (file.type == 'application/x-zip-compressed'){
        // Append the file (zip)
        fd.append('ontologiesZip', file);
    }
    fd.append('patterns_type', typeValue);
    fd.append('flatten_lists', flattenValue);
    // Send the HTTP Post request
    xhr.send(fd);
}

//Click event handler for the button 'download' in order to download the ttl file
//If there is not a transform diagram loaded => warn the user
//If there is a transform diagram loaded => download it
downloadButton.addEventListener('click', ()=>{
    if(loadTransformedDiagram){
        downloadFile('output.zip', response);
    } else{
        alert('There is not loaded a transform diagram');
    }
});


// Function to download a file
function downloadFile(filename, text){
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;base64,' + text);
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}
