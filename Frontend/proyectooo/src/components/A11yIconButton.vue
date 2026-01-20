<template>
  <button
    :type="type"
    class="inline-flex items-center justify-center"
    :aria-label="ariaLabel"
    :title="title || ariaLabel"
    :aria-pressed="ariaPressed"
    :aria-expanded="ariaExpanded"
    :aria-controls="ariaControls"
    v-on="$listeners"
  >
    <i v-if="iconClass" :class="iconClass" aria-hidden="true"></i>
    <span class="sr-only">{{ ariaLabel }}</span>
    <slot />
  </button>
</template>

<script>
export default {
  name: 'A11yIconButton',
  props: {
    ariaLabel: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      default: '',
    },
    iconClass: {
      type: String,
      default: '',
    },
    type: {
      type: String,
      default: 'button',
    },
    ariaPressed: {
      type: [String, Boolean],
      default: null,
    },
    ariaExpanded: {
      type: [String, Boolean],
      default: null,
    },
    ariaControls: {
      type: String,
      default: null,
    },
  },
};
</script>

<style scoped>
</style>


