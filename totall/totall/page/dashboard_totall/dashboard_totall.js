frappe.pages['dashboard-totall'].on_page_load = function(wrapper) {
  frappe.inicio = new frappe.Inicio(wrapper);

  $(".videomodal").attr("data-video-id","qonZrobxvYc");
  $(".js-modal-btn").modalVideo();

}

frappe.Inicio = Class.extend({

  init: function (parent) {
    frappe.ui.make_app_page({
      parent: parent,
      title: "Actividad Reciente",
      single_column: true
    });

    this.parent = parent;
    this.page = this.parent.page;
    this.message = null;
    this.make();
  },

  make: function () {
    var me = this;

   var $container = $(`<div class="page-main-content">
  <div class="row">
    <div class="col-md-6"><div class="clientes-graph"></div></div>
    <div class="col-md-6"><div class="productos-graph"></div></div>
  </div>
  <div class="row">
    <div class="col-md-4">
      <div class="abrirturno panel links-dashboard">
      <a href="#List/Sales Invoice/List"> <img src="/assets/totall/images/abrir_turno.png" width="150">
      <h2>Historial de Ventas</h2>
      <button class="btn btn-primary"> Ver Historial </button></a>
    </div></div>
    <div class="col-md-4"><div class="hacerventa panel links-dashboard">
      <a href="#pov"> <img src="/assets/totall/images/vender.png" width="150">
      <h2>Punto de Venta</h2>
      <button class="btn btn-primary"> Hacer Venta</button></a>
    </div> </div>
    <div class="col-md-4"><div class="otracosa panel links-dashboard">
      <a href="#List/Item/List"> <img src="/assets/totall/images/caja.png" width="150">
      <h2>Articulos</h2>
      <button class="btn btn-primary"> Ver Articulos</button></a>
    </div> </div>
  </div>
</div>`).appendTo(this.page.main);

    this.$graph_area = $container.find('.clientes-graph');
    this.$graph_area_productos = $container.find('.productos-graph');
    me.make_request($container);
  },

  make_request: function ($container) {
    var me = this;
    me.get_clientes( $container);
    me.get_productos( $container);
    console.log('request prod');
  },

  get_clientes: function ($container, start=0) {
    var me = this;

    frappe.call({
      method: "totall.totall.page.dashboard_totall.dashboard_totall.get_clientes",
      args: {
        doctype: "Customer",
        timespan: "Year",
        field: "total_amount",
        start: start
      },
      callback: function (r) {
        let results = r.message || [];
        console.log("results: ",results);

        let graph_items = results.slice(0, 7);
        console.log("graph_items: ",graph_items);

        me.$graph_area.show().empty();
        let args = {
          parent: '.clientes-graph',
          title: "Ventas x Cliente (Top 7)",
          subtitle:"Estos son los clientes con mayor volumen de compra anual",
          data: {
            datasets: [
              {
                values: graph_items.map(d=>d.value)
              }
            ],
            labels: graph_items.map(d=>d.name)
          },
          colors: ['light-blue'],
          format_tooltip_x: d=>d["total_amount"],
          type: 'bar',
          height: 250
        };
        new Chart(args);

      }
    });
  },
  get_productos: function ($container, start=0) {
    var me = this;

    frappe.call({
      method: "totall.totall.page.dashboard_totall.dashboard_totall.get_clientes",
      args: {
        doctype: "Item",
        timespan: "Year",
        field: "mas_vendidos",
        start: start
      },
      callback: function (r) {
        let results = r.message || [];
        console.log("results productos: ",results);

        let graph_items = results.slice(0, 7);
        console.log("graph_items_productos: ",graph_items);

        me.$graph_area_productos.show().empty();
        let args = {
          parent: '.productos-graph',
          title: "Productos Mas Vendidos",
          subtitle:"Estos son los articulos con mas ventas este año.",
          data: {
            datasets: [
              {
                values: graph_items.map(d=>d.value)
              }
            ],
            labels: graph_items.map(d=>d.name)
          },
          colors: ['blue'],
          format_tooltip_x: d=>d["total_amount"],
          type: 'scatter',  // or 'line', 'scatter', 'pie', 'percentage'
          height: 250
        };
        new Chart(args);

      }
    });
  }


});
