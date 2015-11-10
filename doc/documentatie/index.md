# Dynamisch inzicht in de structuur van een applicatielandschap
Een eenvoudige poging om op basis van in Splunk geregistreerde netstat informatie te bepalen wat de structuur van een applicatielandschap is.

## Maak dynamisch een graph

## Hieronder de dot plugin
<dot>
digraph G {
  node [shape=box,
	fontname = "Verdana",
	fontsize = "8" ];
  edge [ 
	fontname = "Verdana",
	fontsize = "8" ];
 subgraph lvbag{
	lvbag_kv->cloudDB_1 [weight=108]; 
	lvbag_kv_cto_eto->cloudDB_4 [weight=96]; 
	lvbag_nfs->lvbag_vs_em [weight=27]; 
	lvbag_vs_audit->ip_10_91_140_200 [weight=12]; 
	lvbag_vs_audit->cloudDB_1 [weight=156]; 
	lvbag_vs_audit->csu117 [weight=12]; 
	lvbag_vs_bw->ESB [weight=48]; 
	lvbag_vs_bw->cloudDB_1 [weight=712]; 
	lvbag_vs_bw->cloudDB_2 [weight=1]; 
	lvbag_vs_bw->cloudDB_3 [weight=4]; 
	lvbag_vs_bw->cloudDB_4 [weight=4]; 
	lvbag_vs_em->ESB [weight=48]; 
	lvbag_vs_em->cloudDB_1 [weight=672]; 
	lvbag_vs_em->csu117 [weight=72]; 
	lvbag_vs_em->lvbag_nfs [weight=53]; 
	lvbag_vs_viewer->lvbag_web [weight=357]; 
	lvbag_vs_viewer->pdok_intern [weight=124]; 
	lvbag_vs_viewer->werkplek [weight=6]; 
	lvbag_web->lvbag_kv [weight=284]; 
	lvbag_web->lvbag_vs_audit [weight=108]; 
	lvbag_web->lvbag_vs_bw [weight=567]; 
	lvbag_web->lvbag_vs_em [weight=6]; 
	lvbag_web_viewer->lvbag_vs_viewer [weight=481]; 
	lvbag_web_viewer->pdok_intern [weight=1386]; 
  }
}
</dot>
