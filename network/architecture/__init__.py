from .loss import l1_regularization
from .loss import supervised_optimal_loss, unsupervised_optimal_loss
from .loss import selfsupervised_optimal_loss, selfsupervised_suboptimal_loss, selfsupervised_suboptimal2_loss
from .loss import unsupervised_suboptimal_loss


from .max_base import MaxModelBase, RelationMessagePassingModel as MaxRelationMessagePassingModel
from .add_base import AddModelBase, RelationMessagePassingModel as AddRelationMessagePassingModel

from .max_numeric_values import MaxNumericModelValues, RelationMessagePassingModel as MaxNumericValuesRelationMessagePassingModel



from .add_numeric_values import AddNumericModelValues, RelationMessagePassingModel as AddNumericValuesRelationMessagePassingModel


from .mean_numeric_values import MeanNumericModelValues, RelationMessagePassingModel as MeanNumericValuesRelationMessagePassingModel
from .smooth_max_numeric_values import SmoothMaxNumericModelValues, RelationMessagePassingModel as SmoothMaxNumericValuesRelationMessagePassingModel

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


from .loss import set_suboptimal_factor, set_loss_constants

# Maps (aggregation, readout, loss, numeric,num_inputs,actions_readout) -> model
g_model_classes = {

    ('max',       False, 'supervised_optimal',False,False,False):         SupervisedOptimalMaxModel,
    ('max',       False, 'base',False,False, False):                       MaxModelBase,
    ('max',       False, 'supervised_optimal',True,False, False):          SupervisedOptimalMaxModel,
    ('max',       False, 'base',True,False, False):                        MaxModelBase,
    ('max',       False, 'base',True,True,False):                         MaxNumericModelValues,
    ('max',       False, 'supervised_optimal',True,True,False):           SupervisedOptimalMaxNumericValuesModel,
    

    ('add',       False, 'base',False,False, False):                       AddModelBase,
    ('add',       False, 'supervised_optimal',False,False, False):         SupervisedOptimalAddModel,
    ('add',       False, 'base',True,False, False):                        AddModelBase,
    ('add',       False, 'supervised_optimal',True,False, False):          SupervisedOptimalAddModel,
    ('add',       False, 'base',True,True, False):                         AddNumericModelValues,
    ('add',       False, 'supervised_optimal',True,True, False):           SupervisedOptimalAddNumericValuesModel,
    ('add',       False, 'supervised_optimal',True,True, True):             SupervisedOptimalAddNumericValuesActionsReadoutModel,

    
    ('mean',      False, 'base',True,True, False):                         MeanNumericModelValues,
    ('mean',      False, 'supervised_optimal',True,True, False):           SupervisedOptimalMeanNumerciValuesModel,
    
    ('smoothmax', False, 'base',True,True, False):                         SmoothMaxNumericModelValues,
    ('smoothmax', False, 'supervised_optimal',True,True, False):           SupervisedOptimalSmoothMaxNumericValuesModel,
}


