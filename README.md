# sid_stock_picking_address

Módulo Odoo (v15) para mover a código la dirección de entrega del albarán (`stock.picking`), sustituyendo la personalización previa en Studio para el campo de dirección de tipo texto.

## Objetivo

Este módulo nace para **estabilizar** una personalización que estaba en Studio y evitar lógica frágil en compute.

### Qué resuelve

- Reemplaza el campo Studio `stock.picking.x_direccion` (Text, no almacenado) por `stock.picking.sid_direccion`.
- Calcula la dirección en Python usando `@api.depends` y asignación directa al campo.
- Inserta el nuevo campo en el formulario de albarán.

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

---

## Instalación

1. Copiar este módulo al path de addons.
2. Actualizar Apps (`-u all` o desde interfaz).
3. Instalar **sid_stock_picking_address**.

Dependencias declaradas:

- `stock`

---

## Resultado esperado

Con este módulo instalado:

- la dirección de entrega deja de depender del compute Studio con `write()`;
- la lógica queda versionada en Git y mantenible;
- el formulario usa `sid_direccion` de forma consistente.
