document.addEventListener("DOMContentLoaded", function(){

const readBtns = document.querySelectorAll(".read-more-btn");
const modals = document.querySelectorAll(".modal");
const closeBtns = document.querySelectorAll(".close-btn");

readBtns.forEach(btn=>{
  btn.addEventListener("click",()=>{
    const id = btn.getAttribute("data-modal");
    const modal = document.getElementById(id);
    if(modal){ modal.style.display="flex"; }
  });
});

closeBtns.forEach(btn=>{
  btn.addEventListener("click",()=>{
    btn.closest(".modal").style.display="none";
  });
});

window.addEventListener("click",(e)=>{
  modals.forEach(modal=>{
    if(e.target===modal){ modal.style.display="none"; }
  });
});

});