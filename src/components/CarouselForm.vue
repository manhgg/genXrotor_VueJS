<template>
  <!-- <div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="../assets/img_1.jpg" class="d-block w-100" width="100" alt="...">
    </div>
    <div class="carousel-item">
      <img src="../assets/img_2.jpg" class="d-block w-100" width="100" alt="...">
    </div>
    <div class="carousel-item">
      <img src="../assets/img_3.jpg" class="d-block w-100" width="100" alt="...">
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div> -->

  <!-- <div>
    <ul>
      <template v-for="path in imgPath" :key="path">
        <li >
          {{path}}
        </li>
      </template>
    </ul>
  </div> -->

  <div
    id="carouselExampleControls"
    class="carousel slide"
    data-bs-ride="carousel"
    :key="updtKey"
  >
    <div class="carousel-inner">
      <template v-for="(path, idx) in imgPath" :key="path">
        <div class="carousel-item" :class="{ active: idx == 0 }">
          <img
            v-bind:src="path"
            class="d-block w-100"
            width="100"
            :alt="path"
          />
        </div>
      </template>
    </div>
    <button
      class="carousel-control-prev"
      type="button"
      data-bs-target="#carouselExampleControls"
      data-bs-slide="prev"
    >
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button
      class="carousel-control-next"
      type="button"
      data-bs-target="#carouselExampleControls"
      data-bs-slide="next"
    >
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>

<script>
import { onMounted } from "@vue/runtime-core";
import { ref } from "vue";
//import Vue from 'vue';
export default {
  name: "CarouselForm",
  props: {},
  setup() {
    let regex = /.*\.jpg/;
    const updtKey = ref(0);
    const isImgPathFilled = ref(false);
    const docuPath = "B:\\Imágenes Respaldo\\Perritos\\"; //process.cwd()+'/src/assets/';////
    var fs = require("fs");
    let imgPath = [];
    const fillCarousel = () => {
      //   //console.log(docuPath)

      fs.readdir(docuPath, (err, files) => {
        if (err) throw err;
        files.forEach(function (file) {
          if (regex.test(file)) {
            imgPath.push(docuPath + file);
            // console.log(file)
          }
        });
        if (imgPath.length > 0) {
          isImgPathFilled.value = true;
          console.log(isImgPathFilled.value);
          imgPath.forEach(function (path) {
            console.log(path);
          });
        }
        forceUpdt();
      });
    };
    fillCarousel();

    const forceUpdt = () => {
      updtKey.value += 1;
    };

    return {
      fillCarousel,
      imgPath,
      isImgPathFilled,
      updtKey,
    };
  },
};
</script>

<style></style>
