document.addEventListener('DOMContentLoaded', function() {

    ///// Header

    // Nav bar button for media queries (tablet or phone)

    let navBarLinks = document.querySelector("#nav-bar-links");

    document.querySelector("#nav-bar-button").onclick = function () {

        if (navBarLinks.style.display === "block") {

            navBarLinks.style.display = "none";
        } 
        else {
            navBarLinks.style.display = "block";
        }
    }

    window.addEventListener("resize", function() {
        if (window.innerWidth > 900) {
            navBarLinks.style.display = "block";
        } 
        else
        {
            navBarLinks.style.display = "none";
        }
    });

    ///// Header - Main page

    // Header update missing weight of user
    let missingWeight = document.querySelector('#missing-weight');
    if (missingWeight != null)
    {

        fetch(`user/api/${missingWeight.dataset.userid}`)
        .then(response => response.json())
        .then(data => {

            missingWeight.innerHTML = Math.abs(data.weight - data.weight_goal);
        })
    }

    // Send message to know features on the app
    let form_message = document.querySelector('#app-message');

    if (form_message != null)
    {
        form_message.onsubmit = function () {

            let message = form_message.children[1];
            message.disabled = true;
            let user_id = message.id.slice(17);
    
            if (message.value.length > 300)
            {
                console.log('Too many characters!');
                return false;
            }
    
            fetch(`send_message/${user_id}`, {
                method: 'POST',
                body: JSON.stringify({
                    message_app: message.value
                })
            })
            .then(response => response.json())
            .then( show => {
                console.log(show)
            })
    
            form_message.children[1].style.display = 'none';
            form_message.children[2].style.display = 'none';
            form_message.children[3].style.display = 'none';
    
            let paragraph = document.createElement('p');
            paragraph.classList.add('flash-message');
            paragraph.innerHTML = 'Message sent! Thank you';
            form_message.append(paragraph);
    
            return false;
        }
    
        // Check max carachters characters
        let textarea = document.querySelector('.textarea-app');
        let max = 300;
    
        textarea.onkeydown = function(event) {
            let carach = document.querySelector('#max-carach');
            let total_ = this.value.length + 1;
    
            if (event.key === 'Backspace')
            {
                this.onkeyup = function() {
                    total_ = this.value.length;
                    carach.innerHTML = max - total_;
                }
            }
            else
            {
                carach.innerHTML = max - total_;
            }
    
        }
    }

    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////

    ///// Recipes

    // Recipes Not logged, to show 3 recipes
    document.querySelectorAll(".recipes-button").forEach( button => {
        
        button.onclick = function() {

            document.querySelectorAll(".recipes__recipe--info").forEach( recipe => {
                recipe.style.display = "none";
            })

            if (button.id === "bulk-recipe")
            {
                document.querySelector(`[data-recipe="bulk-recipe"]`).style.display = "block";
            }
            else if (button.id === "reduce-weight-recipe")
            {
                document.querySelector(`[data-recipe="reduce-weight-recipe"]`).style.display = "block";
            }
            else if (button.id === "healthy-dessert-recipe")
            {
                document.querySelector(`[data-recipe="healthy-dessert-recipe"]`).style.display = "block";
            }
        }
    })

    // Recipes Logged to show recipes list
    let recipesList = document.querySelector('.recipes__list');

    document.querySelectorAll('.cards-button').forEach(button => {
        
        button.onclick = function() {

            let recipesList = document.querySelector('.recipes__list');
            recipesList.innerHTML = "";
            let category = this.dataset.category;

            fetch(`/recipes/api/${category} `)
            .then(response => response.json())
            .then( data => {

                let quantity = 4;
                let start = 0;
                
                createRecipesList(data, start, quantity, category, next_page=true);
 
            })

        }
    })

    // Function to create recipes list
    function createRecipesList(data, start, quantity, category, next_page=true)
    {
        // Declare variables depending if its to go next page or previous
        if (next_page)
        {
            startP = start; 
            end = start + quantity;
            

        } else {
            startP = start - quantity*2; 
            end = start - quantity;
        }

        let recipesList = document.querySelector('.recipes__list');

        for (let i = startP; i < end; i++)
        {
            if (data[i] === undefined)
            {
                break;
            }
            let divListItem = document.createElement('div');
            divListItem.classList.add('recipes__list__item');
            recipesList.append(divListItem);

            let image = document.createElement('img');
            image.classList.add('recipes__list__item__img')
            image.src = data[i].image;
            image.alt = data[i].name;
            divListItem.append(image);

            let divItemInfo = document.createElement('div');
            divItemInfo.classList.add('recipes__list__item__info');
            divListItem.append(divItemInfo);

            let headingTertiary = document.createElement('h3');
            headingTertiary.classList.add('heading-tertiary');
            headingTertiary.innerHTML = data[i].name;
            divItemInfo.append(headingTertiary);

            let paragraph = document.createElement('p');
            paragraph.classList.add('paragraph');
            paragraph.innerHTML = data[i].summary;
            divItemInfo.append(paragraph);

            let link = document.createElement('a');
            link.classList.add('btn', 'btn--citrus', 'margin-top-medium');
            link.innerHTML = 'Check full recipe here';
            link.href = data[i].url_field;
            divItemInfo.append(link); 
        }

        let divPaginator = document.createElement('div');
        divPaginator.classList.add('recipes__list__paginator');
        recipesList.append(divPaginator);

        if (end > quantity)
        {
            let buttonLeft = document.createElement('button');
            buttonLeft.classList.add('recipes__list__paginator__arrow');
            buttonLeft.id = 'next-page-recipes';
            divPaginator.append(buttonLeft);

            let iconLeft = document.createElement('i');
            iconLeft.classList.add('fas', 'fa-arrow-circle-left');
            buttonLeft.append(iconLeft);

            // Pagination
            buttonLeft.addEventListener('click', function() {
                
                let anchor = document.querySelector('#checked');

                anchor.scrollIntoView({behavior:'smooth', block: 'start'});
   
                recipesList.innerHTML = "";

                fetch(`/recipes/api/${category} `)
                .then(response => response.json())
                .then( data => {

                    createRecipesList(data, end, quantity, category, next_page=false);

                })

            });

        }

        if (data.length > end)
        {

            let buttonRight = document.createElement('button');
            buttonRight.classList.add('recipes__list__paginator__arrow');
            buttonRight.id = 'before-page-recipes';
            divPaginator.append(buttonRight);

            let iconRight = document.createElement('i');
            iconRight.classList.add('fas', 'fa-arrow-circle-right');
            buttonRight.append(iconRight);


            // Pagination
            buttonRight.addEventListener('click', function() {

                let anchor = document.querySelector('#checked');
                anchor.scrollIntoView({behavior:'smooth', block: 'start'});

                recipesList.innerHTML = "";

                fetch(`/recipes/api/${category} `)
                .then(response => response.json())
                .then( data => {
                    
                    createRecipesList(data, end, quantity, category);

                })
            });
            
        }

    }


    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////

    ///// Pop up

    // Show Pop up
    document.querySelectorAll('.pop-up-link').forEach( link => {

        link.onclick = function() 
        {            
            document.querySelector(`#${link.dataset.popup}`).style.display = 'block';
            document.querySelector('body').style.overflow = "hidden";

            let bmiTag = document.querySelector('#profile-bmi');

            // BMI Categories:
            // // Underweight = <18.5
            // // Normal weight = 18.5–24.9
            // // Overweight = 25–29.9
            // // Obesity = BMI of 30 or greater

            if (bmiTag != null) 
            {
                fetch(`user/api/${bmiTag.dataset.userid}`)
                .then(response => response.json())
                .then(data => {

                    let bmi = (data.weight / data.height / data.height)*10000;
                    bmi = bmi.toFixed(1);

                    if (bmi < 18.5)
                    {
                        bmiTag.innerHTML = bmi + " (Underweight)";
                    } 
                    else if (bmi > 18.5 && bmi < 24.9)
                    {
                        bmiTag.innerHTML = bmi + " (Normal Weight)";

                    }
                    else if (bmi > 25 && bmi < 29.9)
                    {
                        bmiTag.innerHTML = bmi + " (Overweight)";
                    }
                    else if (bmi > 30)
                    {
                        bmiTag.innerHTML = bmi + " (Obesity)";
                    }
                })
            
            }
        }
    })

    // Close pop up
    document.querySelectorAll('.pop-up-close').forEach( close => {
        close.onclick = function() {
        
            document.querySelector(`#${this.dataset.popup}`).style.display = 'none';
            document.querySelector('body').style.overflowY = "scroll";
        }
    })

    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////

    ///// Food list

    // Food cards
    document.querySelectorAll('.food-list-button').forEach( button => {

        button.onclick = function() {

            // Clear div
            let mainDiv = document.querySelector('#food-list');
            mainDiv.innerHTML = '';
            let user_id = this.dataset.user;

            // User List of foods
            if (this.dataset.list === 'myList')
            {
                // API get users list of foods
                fetch(`user/api/${user_id}`)
                .then( response => response.json())
                .then( data => {

                    let listLenght = data['list-foods'].length; 
                    
                    // Loop thru each food in the list
                    for (let i = 0; i < listLenght; i++)
                    {

                        // API for each food
                        fetch(`food/${data['list-foods'][i]}`)
                        .then(response => response.json())
                        .then( food => {

                            let card = document.createElement('div');
                            card.classList.add('list-card');
                            card.id = food.id;
                            mainDiv.append(card);

                            // Create card
                            createCard(card, food, remove=false);

                            // create button to remove from list
                            createButton(card ,food, add=false, user_id);

                        })
                        
                    }

                })
            }

            // All foods from website plus user created foods
            else if (this.dataset.list === 'allFoods')
            {
                // Get all foods
                fetch('all-foods')
                .then(response => response.json())
                .then( food => {

                    let listLenght = food.length;

                    // Loop thru each food
                    for (let i = 0; i < listLenght; i++)
                    {
                        let card = document.createElement('div');
                        card.classList.add('list-card');
                        card.id = food.id;
                        mainDiv.append(card);

                        // Create card for each food
                        createCard(card, food[i]);

                        userApiButton(card, user_id, food[i]);                  

                    }
                    

                })
            }

            else if (this.dataset.list === 'created')
            {

                // Get all foods created by user
                fetch(`food/user/created/${user_id}`)
                .then(response => response.json())
                .then(foods => {

                    let dataLength = foods.length;
                    for (let i = 0; i < dataLength; i++)
                    {
                        let card = document.createElement('div');
                        card.classList.add('list-card');
                        card.id = foods[i].id;
                        mainDiv.append(card);

                        createCard(card, foods[i], remove=true, user_id=user_id);

                        userApiButton(card, user_id, foods[i]);

                    }
                })

            }
        }
        
    })

    // Search bar - Search food
    let searchFood = document.querySelector('#search-food');
    if (searchFood !== null)
    {
        searchFood.onsubmit = function(){

            // Clear any foods listed
            let mainDiv = document.querySelector('#food-list');
            mainDiv.innerHTML = '';

            // Store values in variables
            let query = this.children[0].value;
            let user_id = this.dataset.userid;

            // Push each query that match food in DB
            let foodsList = [];

            // Query thru all foods
            fetch('all-foods')
            .then(response => response.json())
            .then(data => {

                // console.log(data);

                // Loop thru all foods
                for (let i = 0; i < data.length; i++)
                {
                    // Store food name
                    let food = data[i].name.toLowerCase();

                    // Loop thru all letters of query
                    for (let n = 0; n < query.length; n++)
                    {
                        // If food match letter by letter
                        if (query[n] === food[n])
                        {
                            // If we are in the last loop, save it on array
                            if (n === query.length - 1)
                            {
                                foodsList.push(data[i].id);
                                break;
                            }
                        }
                        // If don't match the query, go to next food
                        else
                        {
                            break;
                        }
                    }
                    
                }

                
            })
            .then(function(){

                // If the matches we got ain't 0
                if (foodsList.length > 0)
                {
                    // Create card for each food
                    for (let u = 0; u < foodsList.length; u++)
                    {
                        fetch(`food/${foodsList[u]}`)
                        .then(response => response.json())
                        .then(food => {

                            let card = document.createElement('div');
                            card.classList.add('list-card');
                            card.id = food.id;
                            mainDiv.append(card);

                            createCard(card, food);

                            userApiButton(card, user_id, food);

                        })
                    }

                }

            })

            // Clear search bar
            this.children[0].value = '';

            // Don't refresh page
            return false;
        }
    }

    // Function to create each card on list of foods
    function createCard(card, food, remove=false, user_id=null)
    {

        // If food was created by user
        // Create button to remove food
        if (remove)
        {
            let span = document.createElement('span');
            span.classList.add('list-card__remove-food');
            card.append(span);

            // When click on button to delete
            // Show pop up 2 factor verification
            span.onclick = function() {
                
                document.querySelector('body').style.overflow = "hidden";

                let popupbox = document.createElement('div');
                popupbox.classList.add('pop-up__box');
                popupbox.style.display = 'block';
                document.querySelector('body').append(popupbox);

                let popup = document.createElement('div');
                popup.classList.add('pop-up');
                popupbox.append(popup);

                let popupHeader = document.createElement('div');
                popupHeader.classList.add('pop-up__header');
                popup.append(popupHeader);

                let popuptitle = document.createElement('h2');
                popuptitle.classList.add('heading-secondary');
                popuptitle.innerHTML = "You sure you want to delete?";
                popupHeader.append(popuptitle);

                let close = document.createElement('span');
                close.classList.add('pop-up__header--close');
                popupHeader.append(close);

                // Close pop up
                close.onclick = function() {
                    popupbox.style.display = 'none';
                    document.querySelector('body').style.overflow = "scroll";
                }

                let form = document.createElement('form');
                form.classList.add('pop-up__form');
                popup.append(form);

                let input = document.createElement('input');
                input.classList.add('btn--warning');
                input.type = 'submit';
                input.value = 'Delete';
                form.append(input);

                // Delete food created by user
                form.onsubmit = function() {

                    // User API
                    fetch(`user/api/${user_id}`, {
                        method: 'DELETE',
                        body: JSON.stringify({
                            food_id: card.id
                        })
                    })
                    .then(function() {
                        card.style.display = 'none';
                        popupbox.style.display = 'none';
                        document.querySelector('body').style.overflow = "scroll";
                    })

                    return false;
                }

            }
        }

        let foodName = document.createElement('h4');
        foodName.classList.add('heading-forth');
        foodName.innerHTML = food.name;
        card.append(foodName);

        let foodBrand = document.createElement('h4');
        foodBrand.classList.add('heading-forth');
        foodBrand.innerHTML = food.brand;
        card.append(foodBrand);

        let nutrition = document.createElement('div');
        nutrition.classList.add('list-card__nutrition-stats');
        card.append(nutrition);

        let calories = document.createElement('p');
        calories.classList.add('list-card__nutrition-stats__info');
        calories.innerHTML = 'Calories:';
        nutrition.append(calories);
        let spanCalories = document.createElement('span');
        spanCalories.innerHTML = food.calories;
        calories.append(spanCalories);

        let total_fat = document.createElement('p');
        total_fat.classList.add('list-card__nutrition-stats__info');
        total_fat.innerHTML = 'Total Fat:';
        nutrition.append(total_fat);
        let spanTotalFat = document.createElement('span');
        spanTotalFat.innerHTML = food.total_fat;
        total_fat.append(spanTotalFat);

        let carbs = document.createElement('p');
        carbs.classList.add('list-card__nutrition-stats__info');
        carbs.innerHTML = 'Carbohydrates:';
        nutrition.append(carbs);
        let spanCarbs = document.createElement('span');
        spanCarbs.innerHTML = food.carbs;
        carbs.append(spanCarbs);

        let fiber = document.createElement('p');
        fiber.classList.add('list-card__nutrition-stats__info');
        fiber.innerHTML = 'Fiber:';
        nutrition.append(fiber);
        let spanfiber = document.createElement('span');
        spanfiber.innerHTML = food.fiber;
        fiber.append(spanfiber);

        let protein = document.createElement('p');
        protein.classList.add('list-card__nutrition-stats__info');
        protein.innerHTML = 'Protein:';
        nutrition.append(protein);
        let spanProtein = document.createElement('span');
        spanProtein.innerHTML = food.protein;
        protein.append(spanProtein);
    }

    // Function to create each button for each card
    function createButton(card, food, add, user_id)
    {
        // Food to get the id to update
        // card to append the button
        // add to know if the button is to add or remove
        // user to send PUT request to update

        let buttonToggle = document.createElement('a');
        buttonToggle.dataset.foodId = food.id;
        buttonToggle.innerHTML = 'Remove from list';
        card.append(buttonToggle);

        if (add === true)
        {
            buttonToggle.classList.add('list-card__button', 'list-card__button--add');
            buttonToggle.innerHTML = 'Add to list';
        }
        else
        {
            buttonToggle.classList.add('list-card__button', 'list-card__button--remove');
            buttonToggle.innerHTML = 'Remove from list';
        }

        buttonToggle.onclick = function() {
            
            if (buttonToggle.classList.contains('list-card__button--remove'))
            {
                buttonToggle.classList.remove('list-card__button--remove');
                buttonToggle.classList.add('list-card__button--add');
                buttonToggle.innerHTML = 'Add to list';

                // Update user food list
                fetch(`user/api/${user_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        option: 'remove',
                        f_id: buttonToggle.dataset.foodId,
                    })
                })
                .then(response => response.json())
                .then(answer => console.log(answer))
                
            } 
            else
            {
                buttonToggle.classList.remove('list-card__button--add');
                buttonToggle.classList.add('list-card__button--remove');
                buttonToggle.innerHTML = 'Remove from list';

                // Update user food list
                fetch(`user/api/${user_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        option: 'add',
                        f_id: buttonToggle.dataset.foodId,
                    })
                })
                .then(response => response.json())
                .then(answer => console.log(answer))
            }
        }
    }

    // Function to decide if food card gets a remove or add button
    function userApiButton(card, user_id, food)
    {

        // User id for request
        // food for create button function and its data
        // card for create button function

        // API to know whats the users favourites foods for button add-remove
        fetch(`user/api/${user_id}`)
        .then( response => response.json())
        .then( data => {
            
            let userFood = data['list-foods'];
            let userListFoods = data['list-foods'].length;

            // If user don't have any food
            if (userListFoods === 0)
            {
                createButton(card, food, add=true, user_id);
            }
            else
            {
                // Discover which food is in users list
                for (let n = 0; n < userListFoods; n++)
                {
                    if (food.id === userFood[n])
                    {
                        createButton(card, food, add=false, user_id);
                        break;
                    }

                    if (n + 1 === userListFoods)
                    {
                        createButton(card, food, add=true, user_id);
                        break;
                    }
                }
            }

        })  
    }

    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////

    ///// Dashboard

    // Show Pop up
    document.querySelectorAll('.pop-up-link').forEach( link => {

        link.onclick = function() 
        {            
            document.querySelector(`#${link.dataset.popup}`).style.display = 'block';
            document.querySelector('body').style.overflow = "hidden";

            // Update food from certain day
            let popup_box = document.querySelector('#pop-up-update-food').children[0];
            let popup_form = popup_box.children[1];

            let food_id = popup_form.children[1];
            food_id.value = this.dataset.foodid;

            let popup_form_foodName = popup_form.children[2];
            popup_form_foodName.innerHTML = this.dataset.foodname;
            
            let span = document.createElement('span');
            span.innerHTML = ` (${this.dataset.foodweight} g)`;
            popup_form_foodName.append(span);

            console.log(popup_form);
            
        }
    })

    // console.log(popup_box);
    // console.log(popup_form);
    // console.log(popup_form_foodName);
    
});