<?php declare(strict_types=1);

namespace {{ cookiecutter.namespace }};

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

#[Route(defaults: ['_routeScope' => ['api']])]
class AdminApiExampleController extends AbstractController
{
    #[Route(
        path: '/api/_action/{{ cookiecutter.plugin_name_with_hyphens }}/example', 
        name: 'api.action.{{ cookiecutter.plugin_name_with_hyphens }}.example', 
        methods: ['GET']
    )]
    public function exampleAction(): JsonResponse
    {
        return new JsonResponse(['success' => true]);
    }
}
