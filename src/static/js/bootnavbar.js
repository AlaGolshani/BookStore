function bootnavbar(el = 'main_navbar', options){
    let defaultOption  ={

    }

    this.init = function(){
        var dropdowns = document.getElementsByClassName("dropdown");
        for (var i = 0; i < dropdowns.length; i++) {
            var dropdown = dropdowns.item(i);
            dropdown.addEventListener("mouseover", function(){
                this.classList.add('show');
                this.getElementsByClassName("dropdown-menu")[0].classList.add('show');
            });
            dropdown.addEventListener("mouseout", function(){
                this.classList.remove('show');
                this.getElementsByClassName("dropdown-menu")[0].classList.remove('show');
            });
        }
    }

    this.init();    
}