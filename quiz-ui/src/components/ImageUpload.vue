<script setup>
import { ref, onMounted, watch } from 'vue';

const emit = defineEmits(['file-change']);
const props = defineProps(['fileDataUrl']);

const isSaving = ref(false);
const fileReader = new FileReader();
const fileInput = ref(null);
const file = ref(null);
const fileDataUrl = ref('');

watch(() => props.fileDataUrl, (newValue, oldValue) => { 
  if (newValue !== oldValue) { 
    fileDataUrl.value = newValue; 
  }
});

onMounted(() => { 
  fileReader.addEventListener( 
    "load", 
    () => { 
      fileDataUrl.value = fileReader.result; 
      isSaving.value = false; 
      emit("file-change", fileDataUrl.value); 
    }, 
    false 
  );
});

function fileChange(event) { 
  isSaving.value = true; 
  const input = event.target; 
  file.value = input.files[0]; 
  fileReader.readAsDataURL(file.value);
}

function clickRemoveImageHandler() { 
  file.value = null; 
  fileDataUrl.value = '';
  emit("file-change", ''); 
  if (fileInput.value) { 
    fileInput.value.value = ''; 
  }
}
</script>

<template> 
  <div>
    <input 
      ref="fileInput"
      type="file" 
      :disabled="isSaving" 
      @change="fileChange" 
      accept="image/jpeg, image/png, image/gif" 
      class="form-control mb-2"
    />
    
    <div v-if="fileDataUrl" class="mt-2">
      <img :src="fileDataUrl" class="img-thumbnail" style="max-height: 200px;" />
      <div class="mt-2">
        <button 
          type="button"
          @click="clickRemoveImageHandler" 
          class="btn btn-sm btn-outline-danger"
        >
          Remove Image
        </button>
      </div>
    </div>
    
    <div v-if="isSaving" class="text-muted">
      Processing image...
    </div>
  </div>
</template>