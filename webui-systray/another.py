from webui import webui

my_window = webui.Window()

my_window.show("""

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DJ Set Layout with Vue</title>
  <script src="./node_modules/vue/dist/vue.global.js"></script>
  <!-- <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script> -->
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body,
    html {
      height: 100vh;
      width: 100vw;
      font-family: Arial, sans-serif;
      overflow: hidden;
    }

    .navbar {
      background: #222;
      padding: 10px;
      display: flex;
      justify-content: space-between;
    }

    .navbar button {
      padding: 8px 12px;
      background: #444;
      color: white;
      border: none;
      cursor: pointer;
    }

    .navbar button:hover {
      background: #666;
    }

    .dj-layout {
      display: flex;
      height: calc(100vh - 50px);
      width: 100vw;
    }

    .panel {
      padding: 10px;
      overflow: auto;
      display: flex;
      flex-direction: column;
    }

    .left,
    .right {
      width: 20%;
      background: #f0f0f0;
    }

    .center {
      flex: 1;
      background: #ddd;
      text-align: center;
    }

    .hidden {
      display: none;
    }

    .tab-bar {
      display: flex;
      flex-direction: column;
      gap: 5px;
      margin-bottom: 10px;
    }

    .tab-bar button {
      padding: 10px;
      background: #ccc;
      border: none;
      cursor: pointer;
      text-align: left;
    }

    .tab-bar button:hover {
      background: #bbb;
    }

    .tab-bar button.active {
      background: #999;
      font-weight: bold;
    }

    .tab-content {
      flex: 1;
      background: #fff;
      padding: 10px;
      border: 1px solid #ccc;
    }
  </style>
</head>

<body>
  <div id="app">
    <nav class="navbar">
      <button @click="togglePanel('left')">Toggle Left Panel</button>
      <button @click="togglePanel('right')">Toggle Right Panel</button>
    </nav>

    <div class="dj-layout">
      <!-- Left Panel -->
      <div class="panel left" :class="{ hidden: !panels.left.visible }">
        <div class="tab-bar">
          <button v-for="tab in panels.left.tabs" :key="tab.id" @click="switchTab('left', tab.id)"
            :class="{ active: panels.left.active === tab.id }">
            {{ tab.label }}
          </button>
        </div>
        <div class="tab-content" v-for="tab in panels.left.tabs" :key="'content-'+tab.id"
          v-show="panels.left.active === tab.id">
          🎛️ Left Panel - {{ tab.label }}
        </div>
      </div>

      <!-- Center Panel -->
      <div class="panel center">
        <h2>Main DJ Controls</h2>
      </div>

      <!-- Right Panel -->
      <div class="panel right" :class="{ hidden: !panels.right.visible }">
        <div class="tab-bar">
          <button v-for="tab in panels.right.tabs" :key="tab.id" @click="switchTab('right', tab.id)"
            :class="{ active: panels.right.active === tab.id }">
            {{ tab.label }}
          </button>
        </div>
        <div class="tab-content" v-for="tab in panels.right.tabs" :key="'content-'+tab.id"
          v-show="panels.right.active === tab.id">
          🎛️ Right Panel - {{ tab.label }}
        </div>
      </div>
    </div>
  </div>

  <script>
    const {createApp, ref} = Vue;

    createApp({
      setup() {
        const panels = ref({
          left: {
            visible: true,
            active: 'a1',
            tabs: [
              {id: 'a1', label: 'Deck A1'},
              {id: 'a2', label: 'Deck A2'}
            ]
          },
          right: {
            visible: true,
            active: 'b1',
            tabs: [
              {id: 'b1', label: 'Deck B1'},
              {id: 'b2', label: 'Deck B2'}
            ]
          }
        });

        const togglePanel = (side) => {
          panels.value[side].visible = !panels.value[side].visible;
        };

        const switchTab = (side, tabId) => {
          panels.value[side].active = tabId;
        };

        return {panels, togglePanel, switchTab};
      }
    }).mount('#app');
  </script>
</body>

</html>
""")

webui.wait()
