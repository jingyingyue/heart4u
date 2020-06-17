document.addEventListener('DOMContentLoaded', () => {

    var img = new Image();
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    var fileName = '';
    var filters = {};

     // when user clicks on choose file button
    document.getElementById("upload-file").onchange = function() {
        // get uploaded file, create filereader
        var file = document.querySelector('#upload-file').files[0];
        var reader = new FileReader();

        // read file content using filereader
        if (file) {
            fileName = file.name;
            reader.readAsDataURL(file);
        };

        reader.addEventListener("load", function () {
            // create image
            img = new Image();
            img.src = reader.result;
            
            img.onload = function () {
                // reset canvas width and height for new image
                canvas.width = canvas.width;
                canvas.height = canvas.height;

                // scale image to fit in canvas
                var scale = Math.min(canvas.width/img.width, canvas.height/img.height);
                var x = (canvas.width/2)-(img.width/2)*scale;
                var y = (canvas.height/2)-(img.height/2)*scale;

                // draw image on canvas
                ctx.drawImage(img, x, y, img.width*scale, img.height*scale);
                canvas.removeAttribute('data-caman-id');
            };
        }, false);
    };


    // when user clicks on share photo button
    document.getElementById('share-btn').onclick = () => {
        // update image's input value to its data URI
        document.getElementById('uploaded-pic').value = canvas.toDataURL();
    };


    // apply brightness filter
    document.getElementById('brightness-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.brightness(10).render();
        });
    };

    document.getElementById('brightness-dec').onclick = function() {
        Caman('#canvas', img, function() {
            this.brightness(-10).render();
        });
    };


    // apply contrast filter
    document.getElementById('contrast-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.contrast(10).render();
        });
    };

    document.getElementById('contrast-dec').onclick = function() {
        Caman('#canvas', img, function() {
            this.contrast(-10).render();
        });
    };


    // apply saturation filter
    document.getElementById('saturation-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.saturation(10).render();
        });
    };

    document.getElementById('saturation-dec').onclick = function() {
        Caman('#canvas', img, function() {
            this.saturation(-10).render();
        });
    };


    // apply vibrance filter
    document.getElementById('vibrance-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.vibrance(10).render();
        });
    };

    document.getElementById('vibrance-dec').onclick = function() {
        Caman('#canvas', img, function() {
            this.vibrance(-10).render();
        });
    };


    // apply exposure filter
    document.getElementById('exposure-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.exposure(10).render();
        });
    };

    document.getElementById('exposure-dec').onclick = function() {
        Caman('#canvas', img, function() {
            this.exposure(-10).render();
        });
    };


    // apply noise filter
    document.getElementById('noise-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.noise(10).render();
        });
    };


    // apply sharpen filter
    document.getElementById('sharpen-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.sharpen(10).render();
        });
    };


    // apply sepia filter
    document.getElementById('sepia-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.sepia(20).render();
        });
    };


    // apply hue filter
    document.getElementById('hue-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.hue(10).render();
        });
    };


    // apply blur filter
    document.getElementById('blur-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.stackBlur(5).render();
        });
    };


    // apply gamma filter
    document.getElementById('gamma-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.gamma(0.1).render();
        });
    };


    // apply clip filter
    document.getElementById('clip-inc').onclick = function() {
        Caman('#canvas', img, function() {
            this.clip(10).render();
        });
    };


    // revert all filters
    document.getElementById('revert-btn').onclick = function() {
        Caman('#canvas', img, function() {
            this.revert();
        });
    };

});