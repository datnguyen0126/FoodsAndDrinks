<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col bg-dark text-white">
                <a class="navbar-brand">Da Nang Milktea</a>
                <div>URL: {{ url }}</div> 
            </div>
        </div>
        <div class="row">

        </div>
    </div>
</template>

<script>
    export default {
        data() { 
            return { 
                url: process.env.VUE_APP_DJANGO_HOST, 
            }
        }
    }
</script>
