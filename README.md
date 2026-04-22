# sid_stock_picking_address

Módulo Odoo (v15) para mover a código la dirección de entrega del albarán (`stock.picking`) y su impresión en el reporte batch, sustituyendo la personalización previa en Studio para el campo `x_direccion` de tipo texto.

## Objetivo

Este módulo nace para **estabilizar** una personalización que estaba en Studio y evitar lógica frágil en compute.

### Qué resuelve

- Reemplaza el campo Studio `stock.picking.x_direccion` (Text, no almacenado) por `stock.picking.sid_direccion`.
- Calcula la dirección en Python usando `@api.depends` y asignación directa al campo.
- Inserta el nuevo campo en el formulario de albarán.
- Sustituye el uso de `o.x_direccion` por `o.sid_direccion` en el reporte batch heredado.

### Qué **no** resuelve (a propósito)

- **No migra** el `x_direccion` de `stock.picking.batch` (Many2one), ya que es otro campo distinto.
- **No desactiva automáticamente** vistas Studio; se recomienda hacerlo tras validar en entorno.

---

## Alcance funcional

## 1) Modelo: `stock.picking`

Se define el campo:

- `sid_direccion` (`fields.Text`)
- `compute="_compute_sid_direccion"`
- `store=False`
- `readonly=True`

Dependencias del cálculo:

- `partner_id`
- `partner_id.street`
- `partner_id.street2`
- `partner_id.city`
- `partner_id.state_id`
- `partner_id.zip`

Regla de cálculo:

- Si no hay partner, devuelve `""`.
- Si hay partner, concatena calle, calle 2, ciudad, provincia y CP, con salto de línea entre bloques no vacíos.

## 2) Vista formulario de albarán

Se hereda `stock.view_picking_form` e inserta `sid_direccion` justo antes de `is_return_picking`.

## 3) Reporte batch (QWeb)

Se hereda `stock_picking_batch.report_picking_batch_copy_1` para imprimir `o.sid_direccion` en ambas columnas de dirección.

Para mantener saltos de línea en PDF se usa:

- `t-esc="o.sid_direccion"`
- `style="white-space: pre-line;"`

---

## Instalación

1. Copiar este módulo al path de addons.
2. Actualizar Apps (`-u all` o desde interfaz).
3. Instalar **sid_stock_picking_address**.

Dependencias declaradas:

- `stock`
- `stock_picking_batch`

---

## Plan de despliegue recomendado (migración segura)

Tras instalar el módulo y validar en QA/UAT:

1. Verificar formulario de `stock.picking`.
2. Verificar PDF del batch picking.
3. Desactivar vistas Studio reemplazadas (si aplica en tu BD):

```python
env['ir.ui.view'].browse([2625, 3034]).write({'active': False})
env.cr.commit()
```

4. **No desactivar** la 3035 sin análisis: corresponde al `x_direccion` de `stock.picking.batch` (Many2one).
5. Mantener temporalmente el campo Studio viejo hasta confirmar que no hay referencias activas.

---

## Validaciones útiles en Odoo shell

### Buscar referencias activas a `x_direccion`

```python
views = env['ir.ui.view'].with_context(active_test=False).search([
    ('arch_db', 'ilike', 'x_direccion'),
])
for v in views:
    print(v.id, v.name, v.active, v.model, v.type)
```

### Verificar campos homónimos por modelo

```python
fields_found = env['ir.model.fields'].search([
    ('name', '=', 'x_direccion'),
    ('model', 'in', ['stock.picking', 'stock.picking.batch']),
])
for f in fields_found:
    print(
        'id=', f.id,
        'model=', f.model,
        'name=', f.name,
        'ttype=', f.ttype,
        'store=', f.store,
        'readonly=', f.readonly,
        'depends=', f.depends,
        'compute=', f.compute,
    )
```

---

## Riesgos conocidos

- Si cambia la estructura base del QWeb `stock_picking_batch.report_picking_batch_copy_1`, los `xpath` pueden requerir ajuste.
- Si otra capa Studio hereda la misma zona de formulario/reporte, puede haber conflictos por prioridad.
- El saneamiento total de Studio debe planificarse por fases para no romper personalizaciones de `stock.picking.batch`.

---

## Resultado esperado

Con este módulo instalado:

- la dirección de entrega deja de depender del compute Studio con `write()`;
- la lógica queda versionada en Git y mantenible;
- formulario y reporte usan `sid_direccion` de forma consistente.
