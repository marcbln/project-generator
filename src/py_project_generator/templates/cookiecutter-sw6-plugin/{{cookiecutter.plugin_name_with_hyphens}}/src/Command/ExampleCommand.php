<?php declare(strict_types=1);

namespace {{ cookiecutter.namespace }};

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Attribute\AsCommand;

#[AsCommand(
    name: '{{ cookiecutter.plugin_name_with_hyphens }}:example',
    description: 'Example command for {{ cookiecutter.plugin_name }} plugin'
)]
class ExampleCommand extends Command
{
    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $output->writeln('<info>{{ cookiecutter.plugin_name }} plugin example command executed successfully!</info>');
        $output->writeln('This is a minimal example command to get you started.');
        
        return Command::SUCCESS;
    }
}
