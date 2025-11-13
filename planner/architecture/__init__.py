from .loss import l1_regularization
from .loss import supervised_optimal_loss, unsupervised_optimal_loss
from .loss import selfsupervised_optimal_loss, selfsupervised_suboptimal_loss, selfsupervised_suboptimal2_loss
from .loss import unsupervised_suboptimal_loss


from .max_base import MaxModelBase, RelationMessagePassingModel as MaxRelationMessagePassingModel
from .add_base import AddModelBase, RelationMessagePassingModel as AddRelationMessagePassingModel

from .max_numeric_values import MaxNumericModelValues, RelationMessagePassingModel as MaxNumericValuesRelationMessagePassingModel



from .add_numeric_values import AddNumericModelValues, RelationMessagePassingModel as AddNumericValuesRelationMessagePassingModel

from .add_numeric_values_actions_readout import AddNumericActionsModelValues, RelationMessagePassingModel as AddNumericValuesActionsReadoutRelationMessagePassingModel

from .mean_numeric_values import MeanNumericModelValues, RelationMessagePassingModel as MeanNumericValuesRelationMessagePassingModel
from .smooth_max_numeric_values import SmoothMaxNumericModelValues, RelationMessagePassingModel as SmoothMaxNumericValuesRelationMessagePassingModel
#from .attention_base import AttentionModelBase, RelationMessagePassingModel as AttentionRelationMessagePassingModel
#from .add_max_base import AddMaxModelBase, RelationMessagePassingModel as AddMaxRelationMessagePassingModel

# Max models
from .model import SupervisedOptimalMaxModel
from .model import SupervisedOptimalMaxNumericValuesModel



#add models
from .model import SupervisedOptimalAddModel
from .model import SupervisedOptimalAddNumericValuesModel
from .model import SupervisedOptimalAddNumericValuesActionsReadoutModel


#mean models
from .model import SupervisedOptimalMeanNumerciValuesModel

#smooth-max models
from .model import SupervisedOptimalSmoothMaxNumericValuesModel
# Attention models
#from .model import SupervisedOptimalAttentionModel, SelfsupervisedSuboptimalAttentionModel, SelfsupervisedOptimalAttentionModel, UnsupervisedOptimalAttentionModel, UnsupervisedSuboptimalAttentionModel, OnlineOptimalAttentionModel
# Add-max models
#from .model import SupervisedOptimalAddMaxModel, SelfsupervisedSuboptimalAddMaxModel, SelfsupervisedOptimalAddMaxModel, UnsupervisedOptimalAddMaxModel, UnsupervisedSuboptimalAddMaxModel, OnlineOptimalAddMaxModel
# Models for new loss
#from .model import SelfsupervisedSuboptimalAddModel2, SelfsupervisedSuboptimalMaxModel2, SelfsupervisedSuboptimalAddMaxModel2, SelfsupervisedSuboptimalMaxReadoutModel2

# Settings
#from .model import set_max_trace_length
from .loss import set_suboptimal_factor, set_loss_constants

# Maps (aggregation, readout, loss, numeric,num_inputs) -> model
g_model_classes = {

    ('max',       False, 'supervised_optimal',False,False):         SupervisedOptimalMaxModel,
    ('max',       False, 'base',False,False):                       MaxModelBase,
    ('max',       False, 'supervised_optimal',True,False):          SupervisedOptimalMaxModel,
    ('max',       False, 'base',True,False):                        MaxModelBase,
    ('max',       False, 'base',True,True):                         MaxNumericModelValues,
    ('max',       False, 'supervised_optimal',True,True):           SupervisedOptimalMaxNumericValuesModel,
    

    ('add',       False, 'base',False,False):                       AddModelBase,
    ('add',       False, 'supervised_optimal',False,False):         SupervisedOptimalAddModel,
    ('add',       False, 'base',True,False):                        AddModelBase,
    ('add',       False, 'supervised_optimal',True,False):          SupervisedOptimalAddModel,
    ('add',       False, 'base',True,True, False):                         AddNumericModelValues,
    ('add',       False, 'supervised_optimal',True,True):           SupervisedOptimalAddNumericValuesModel,
    ('add',       True, 'base',True,True):                           AddNumericActionsModelValues,
    ('add',       True, 'supervised_optimal',True,True):             SupervisedOptimalAddNumericValuesActionsReadoutModel,

    
    ('mean',      False, 'base',True,True):                         MeanNumericModelValues,
    ('mean',      False, 'supervised_optimal',True,True):           SupervisedOptimalMeanNumerciValuesModel,
    
    ('smoothmax', False, 'base',True,True):                         SmoothMaxNumericModelValues,
    ('smoothmax', False, 'supervised_optimal',True,True):           SupervisedOptimalSmoothMaxNumericValuesModel,
}


