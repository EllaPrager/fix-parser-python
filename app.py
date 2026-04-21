import streamlit as st
import pandas as pd

from parser import parse_fix_message, enrich_fix_message, generate_message_summary, validate_fix_message

st.set_page_config(
    page_title="Tagora FIX Decoder",
    layout="wide"
)

st.title("Tagora FIX Decoder")

fix_input = st.text_area(
    "Paste your FIX message",
    height=130,
    placeholder="35=8|150=2|39=2|17=E12345|37=O67890|54=1|55=EUR/USD|38=1000000|44=1.1050|60=20260418-21:32:45.123"
)

if st.button("Decode"):

    if fix_input.strip() == "":
        st.warning("Please paste a FIX message.")
    else:
        parsed_fix = parse_fix_message(fix_input)
        warnings = validate_fix_message(parsed_fix)
        summary = generate_message_summary(parsed_fix)
        enriched = enrich_fix_message(parsed_fix)

        df = pd.DataFrame(enriched)

        st.subheader("Message Summary")

        # colors
        status = summary.get("order_status")
        status_color = "#22c55e"

        if status == "Rejected":
            status_color = "#ef4444"
        elif status == "Pending":
            status_color = "#f59e0b"
        elif status == "Canceled":
            status_color = "#9ca3af"

        side = summary.get("side")
        side_color = "#22c55e"

        if side == "Sell":
            side_color = "#ef4444"

        # build html only for existing fields
        msg_type_html = ""
        if "message_type" in summary:
            msg_type_html = f"<b>Message Type:</b> {summary['message_type']} <br>"

        symbol_html = ""
        if "symbol" in summary:
            symbol_html = f"<b>Symbol:</b> {summary['symbol']} <br>"

        side_html = ""
        if "side" in summary:
            side_html = f"""
<b>Side:</b>
<span style="color:{side_color}; font-weight:600;">
{summary['side']}
</span><br>
"""

        quantity_html = ""
        if "quantity" in summary:
            quantity_html = f"<b>Quantity:</b> {summary['quantity']} <br>"

        price_html = ""
        if "price" in summary:
            price_html = f"<b>Price:</b> {summary['price']} <br>"

        order_type_html = ""
        if "order_type" in summary:
            order_type_html = f"<b>Order Type:</b> {summary['order_type']} <br>"

        order_status_html = ""
        if "order_status" in summary:
            order_status_html = f"""
<b>Order Status:</b>
<span style="color:{status_color}; font-weight:600;">
{summary['order_status']}
</span><br>
"""

        cl_ord_id_html = ""
        if "cl_ord_id" in summary:
            cl_ord_id_html = f"""
<b>ClOrdID:</b>
<code style="color:#93c5fd; background:transparent;">{summary['cl_ord_id']}</code><br>
"""

        order_id_html = ""
        if "order_id" in summary:
            order_id_html = f"""
<b>OrderID:</b>
<code style="color:#93c5fd; background:transparent;">{summary['order_id']}</code><br>
"""
        exec_id_html = ""
        if "exec_id" in summary:
                exec_id_html = f"<b>Execution ID:</b> {summary['exec_id']} <br>"


        exec_type_html = ""
        if "exec_type" in summary:
                exec_type_html = f"<b>Execution Type:</b> {summary['exec_type']} <br>"


        transact_time_html = ""
        if "transact_time" in summary:
            transact_time_html = f"<b>TransactTime:</b> {summary['transact_time']} <br>"

        
        time_in_force_html = ""
        if "time_in_force" in summary:
            time_in_force_html = f"<b>TimeInForce:</b> {summary['time_in_force']} <br>"

        # LastQty - last_qty
        last_qty_html = ""
        if "last_qty" in summary:
            last_qty_html = f"<b>LastQty:</b> {summary['last_qty']} <br>"
        
        #LastPx - last_price
        last_price_html = ""
        if "last_price" in summary:
            last_price_html = f"<b>LastPx:</b> {summary['last_price']} <br>"

        cum_qty_html = ""
        # CumQty - cum_qty
        if "cum_qty" in summary:
            cum_qty_html = f"<b>CumQty:</b> {summary['cum_qty']} <br>"

        leaves_qty_html = ""
        # LeavesQty - leaves_qty
        if "leaves_qty" in summary:
            leaves_qty_html = f"<b>LeavesQty:</b> {summary['leaves_qty']} <br>"

        # SenderCompID - sender_comp_id
        sender_comp_id_html = ""
        if "sender_comp_id" in summary:
            sender_comp_id_html = f"<b>SenderCompID:</b> {summary['sender_comp_id']} <br>"
            
        # TargetCompID - target_comp_id
        target_comp_id_html = "" 
        if "target_comp_id" in summary:
            target_comp_id_html = f"<b>TargetCompID:</b> {summary['target_comp_id']} <br>"

        # orig_cl_ord_id
        orig_cl_ord_id_html = "" 
        if "orig_cl_ord_id" in summary:
            orig_cl_ord_id = f"<b>orig_cl_ord_id:</b> {summary['orig_cl_ord_id']} <br>"

        # text
        text = "" 
        if "text" in summary:
            text = f"<b>text:</b> {summary['text']} <br>"
        
        # sending_time
        sending_time = "" 
        if "sending_time" in summary:
            sending_time = f"<b>sending_time:</b> {summary['sending_time']} <br>"


        st.markdown(f"""
<div style="
padding:22px;
border-radius:14px;
background:#0f172a;
border:1px solid #1f2937;
color:white;
">

<h3 style="margin-top:0;">Message Summary</h3>

<h4>Message Info </h4>
{msg_type_html}
{exec_type_html}
{order_status_html}

<hr style="border-color:#1f2937;">

<h4>Instrument </h4>

{symbol_html}

<hr style="border-color:#1f2937;">


<h4>Order Details </h4>
{side_html}
{order_type_html}
{quantity_html}
{price_html}
{time_in_force_html}

<hr style="border-color:#1f2937;">

<h4>Execution Details </h4>
{last_qty_html}
{last_price_html}
{cum_qty_html}
{leaves_qty_html}

<hr style="border-color:#1f2937;">

<h4>IDs </h4>
{cl_ord_id_html}
{order_id_html}
{exec_id_html}

<hr style="border-color:#1f2937;">

<h4>Routing </h4>
{sender_comp_id_html}
{target_comp_id_html}

<hr style="border-color:#1f2937;">

<h4>Time </h4>
{transact_time_html}


</div>
""", unsafe_allow_html=True)

        st.divider()
        
    #Validation Warnings UI

        if warnings:
            st.markdown("""
                <div style="
                padding:18px;
                border-radius:12px;
                background:#1f2937;
                border:1px solid #374151;
                color:white;
                margin-bottom:20px;
                ">

                <h4 style="margin-top:0; color:#f59e0b;">
                Validation Warnings
                </h4>

                </div>
                """, unsafe_allow_html=True)
            
            for w in warnings:
                st.warning(w)

        st.subheader("Decoded Fields")
        st.dataframe(df, width="stretch")