class BuildInfo:

    def __init__(self, client):
        self.client = client
        self.study_type = ''
        self.subtype = ''
        self.design_type = ''
        self.design_model = ''
        self.runs = 0
        self.blocks = 0
        self.groups = 0
        self.build_time = 0
        self.center_points = 0

        result = self.client.send_payload({
            "method": "GET",
            "uri": "information/summary/build",
        })

        for k, v in result['payload'].items():
            setattr(self, k, v)


    def __str__(self):
            return """Build Information
Study Type: {study_type}
Subtype: {subtype}
Design Type: {design_type}
Design Model: {design_model}
Runs: {runs}
Blocks: {blocks}
Groups: {groups}
Build Time (ms): {build_time}
Center Points: {center_points}
Properties: {properties}""".format(
                study_type=self.study_type,
                subtype=self.subtype,
                design_type=self.design_type,
                design_model=self.design_model,
                runs=self.runs,
                blocks=self.blocks,
                groups=self.groups,
                build_time=self.build_time,
                center_points=self.center_points,
                properties=self.properties
            )


class Evaluation:

    def __init__(self, client):
        self.client = client
        result = self.client.send_payload({
            "method": "GET",
            "uri": "information/evaluation/dof",
        })

        for k, v in result['payload'].items():
            setattr(self, k, v)

    def __str__(self):
        model_terms = "Model Terms\n"
        model_terms += "Term: %s\n"%self.terms
        model_terms += "Standard Error: %s\n"%self.std_error
        if self.error_df:
            model_terms += "Error df: %s\n"%self.error_df
        if self.vif:
            model_terms += "VIF: %s\n"%self.vif
        if self.restricted_vif:
            model_terms += "Restricted VIF: %s\n"%self.restricted_vif
        if self.r2:
            model_terms += "R2: %s\n"%self.r2
        model_terms += "Power: %s\n"%self.power
        
        dof = "Degrees of Freedom\n"
        if self.blocks!="":
           dof += "Blocks: %s\n"%(self.blocks)
        if self.whole_plot:
            dof += "Whole-plot:\n"
            dof += "Model: %s\n"%self.whole_plot[0]['model']
            if self.whole_plot[0]['residuals']!="":
                dof += "Residuals: %s\n"%self.whole_plot[0]['residuals']
            dof += "Total: %s\n"%self.whole_plot[0]['total']
        if self.subplot:
            dof += "Subplot:\n"
            dof += "Model: %s\n"%self.subplot[0]['model']
            if self.subplot[0]['residuals']!="":
                dof += "Residuals: %s\n"%self.subplot[0]['residuals']
            dof += "Total: %s\n"%self.subplot[0]['total']
        else:
            dof += "Model: %s\n"%(self.model)
            dof += "Residuals: %s (Lack of Fit: %s, Pure Error: %s) \n"%(self.residuals[0]['lack_of_fit']+self.residuals[0]['pure_error'], self.residuals[0]['lack_of_fit'], self.residuals[0]['pure_error'])
            dof += "Corr Total: %s\n"%(self.corr_total)
        
        leverage = "Leverage\n"
        leverage += "Run: %s\n"%(self.run)
        leverage += "Leverage: %s\n"%(self.leverage)
        leverage += "Space Type: %s\n"%(self.space_type)
        
        eval_str = model_terms +"\n"+ dof +"\n"+ leverage
        return eval_str