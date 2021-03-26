<template>
  <div class="about">
      <section class="about__header">
        <h1 class="about__title">Co-Meet ?</h1>
      </section>
  </div>
</template>

<script>
export default {

}
</script>

<style lang=scss>
  @mixin borderLayout($color) {
    border: 3px solid $color;
    border-radius: 5px;
    padding: 1rem;
  } 

  .about {
    @include borderLayout(grey); 
    margin-top: 1em;
    
  }
</style>